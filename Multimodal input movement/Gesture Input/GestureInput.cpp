#include <iostream>
#include <SDL.h>
#include <SDL_thread.h>

#include <WinSock2.h>
#include <comdef.h>
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#define SCK_VERSION2 0x0202

#include <Kinect.h>
#include <Kinect.VisualGestureBuilder.h>

// Window dimentions
#define WINDOW_WIDTH 1920
#define WINDOW_HEIGHT 1080
#define VIDEO_WIDTH 640/4
#define VIDEO_HEIGHT 480/4

#define PORT 5028

// Buffer length for receiving video images
#define BUFFER_SIZE 65536

// Global Variables
std::string nameOfGesture[6];					// The names of the gestures
IKinectSensor *gSensor = nullptr;				// Pointer to Kinect sensor
IColorFrameReader *gColorFrameReader = nullptr;	// Color frame reader
IBodyFrameReader *gBodyFrameReader = nullptr;	// Body frame reader
ICoordinateMapper* gCoordinateMapper = nullptr;	// Mapper for joint position
IVisualGestureBuilderFrameSource* gVgbFrameSource = nullptr;	// Frame Source for custom gestures
IVisualGestureBuilderFrameReader *gVgbFrameReader = nullptr;	// Reader for custom gestures
IVisualGestureBuilderDatabase *gGestureDatabase;	// The gesture database
UINT gGestureCount = 0;								// Custom Gesture Count
IGesture **gGestures = nullptr;					// The gestures
SDL_Window* window = nullptr;			// The display window
SDL_Renderer* renderer = nullptr;		// The window renderer
SDL_Texture* windowTexture = nullptr;	// The texture to be rendered
SDL_Texture *videoTexture = nullptr;	// The video texture to be rendered
SDL_Rect videoViewport;					// Viewport for rendering video feed
SDL_Rect windowViewport;				// Viewport for rendering kinect frames
Uint32* pixelBuffer = nullptr;			// Pixel buffer that contains the kinect frames
unsigned char *videoBuffer = nullptr;	// Buffer that contains the video feed from robot
SOCKET socketConnection;				// Socket for robot connection				
bool connected = false;					// Connection with robot flag
HRESULT hr;								// Error checking
int dataSize = VIDEO_HEIGHT * VIDEO_WIDTH * 3;	// Size of received video image
bool videoImageReady = false;			// Flag for received image
bool askForImage = true;				// Flag for asking for next image
const char* robotIp;


struct bodyTracked {
	bool tracked = false;
	Uint64 bodyId = 0;
};

// Safe way of deleting kinect pointers
template<typename T>
void SafeRelease(T &ptr) {
	if (ptr) {
		ptr->Release();
		ptr = nullptr;
	}
}


void error(int i) {
	if (i < 0) {
		std::cout << "SDL Error " << i << ": " << SDL_GetError() << std::endl;
	}
	else if (i > 0) {
		_com_error err(hr);
		LPCTSTR errMsg = err.ErrorMessage();
		std::cout << "Kinect Error " << i << ": ";
		std::wcout << errMsg << std::endl;
	}
}

// Thread that handles the connection with the robot
int socketThread(void* data) {
	SOCKADDR_IN address;
	socketConnection = socket(AF_INET, SOCK_STREAM, NULL);
	if (socketConnection == INVALID_SOCKET) {
		std::cout << "Socket could not be created!" << std::endl;
	}
	//printf("Enter robot ip address: ");
	//scanf("%s", &robotIp);
	address.sin_addr.s_addr = inet_addr(/*"172.20.10.2"*/"192.168.1.32");
	address.sin_family = AF_INET;
	address.sin_port = htons(PORT);

	int result = SOCKET_ERROR;

	do {
		// Try to connect
		printf("Trying to connect . . .\n");
		result = connect(socketConnection, (SOCKADDR*)&address, sizeof(address));
		if (result == 0) {
			connected = true;
			printf("Connected!\n");
		}
		SDL_Delay(1000);
	} while (!connected);

	return 0;
}

// Thread that receives the video camera images
int videoThread(void *data) {
	const char ASKVIDEO[8] = "ASK";
	char buffer[BUFFER_SIZE];		// Buffer for received video images
	int iResult = 0;				// Result of received socket packets
	int pos = 0;					

	do {
		if (connected && askForImage) {
			// Ask for video image
			videoImageReady = false;
			pos = 0;
			send(socketConnection, ASKVIDEO, 3, 0);
			do {
				iResult = recv(socketConnection, buffer, BUFFER_SIZE, 0);
				if (iResult > 0) {
					// Copy socket packet onto videoBuffer
					//std::cout << "Bytes received: " << iResult << std::endl;
					memcpy(&videoBuffer[pos], (unsigned char*)buffer, iResult);
					pos += iResult;
					if (pos == dataSize) {
						videoImageReady = true;
						askForImage = false;
					}
				}
				else if (iResult == 0) {
					// Image is ready for rendering
					printf("Data received!\n");
					videoImageReady = true;
					SDL_Delay(100);
				}
				else {
					std::cout << "Recv failed: " << WSAGetLastError() << std::endl;
					connected = false;
					videoImageReady = false;
					return 0;
				}
			} while (iResult > 0 && pos != dataSize);
		}
	} while (true);


	return 0;
}

// Retrieve gesture name string
std::string gestureName(IGesture* gest) {
	std::wstring buffer(BUFSIZ, L' ');
	hr = gest->get_Name(BUFSIZ, &buffer[0]);
	if (FAILED(hr)) {
		error(14);
		return false;
	}
	const std::wstring::size_type last = buffer.find_last_not_of(L' ');
	if (last == std::wstring::npos) {
		throw std::runtime_error("failed " __FUNCTION__);
	}
	const std::wstring temp = buffer.substr(0, last);
	const std::string name(temp.begin(), temp.end());

	return name;
}

bool kinectInit() {

	// Assign the Kinect sensor
	hr = GetDefaultKinectSensor(&gSensor);
	if (FAILED(hr)) {
		error(4);
		return false;
	}
	gSensor->Open();

	// Get color frame source
	IColorFrameSource *colorFrameSource;
	hr = gSensor->get_ColorFrameSource(&colorFrameSource);
	if (FAILED(hr)) {
		error(5);
		return false;
	}

	// Get color frame reader
	hr = colorFrameSource->OpenReader(&gColorFrameReader);
	if (FAILED(hr)) {
		error(6);
		return false;
	}
	SafeRelease(colorFrameSource);

	// Get body frame source
	IBodyFrameSource *bodyFrameSource;
	hr = gSensor->get_BodyFrameSource(&bodyFrameSource);
	if (FAILED(hr)) {
		error(7);
		return false;
	}

	// Get body frame reader
	hr = bodyFrameSource->OpenReader(&gBodyFrameReader);
	if (FAILED(hr)) {
		error(8);
		return false;
	}
	SafeRelease(bodyFrameSource);

	// Initialize the coordinate mapper
	hr = gSensor->get_CoordinateMapper(&gCoordinateMapper);
	if (FAILED(hr)) {
		error(9);
		return false;
	}

	// Initialize gesture builder database
	hr = CreateVisualGestureBuilderDatabaseInstanceFromFile(L"RobotControl.gbd", &gGestureDatabase);
	if (FAILED(hr)) {
		error(10);
		return false;
	}

	// Initialize frame Source
	hr = CreateVisualGestureBuilderFrameSource(gSensor, 0, &gVgbFrameSource);
	if (FAILED(hr)) {
		error(11);
		return false;
	}

	// Open frame reader
	hr = gVgbFrameSource->OpenReader(&gVgbFrameReader);
	if (FAILED(hr)) {
		error(12);
		return false;
	}

	// Load Gestures
	gGestureDatabase->get_AvailableGesturesCount(&gGestureCount);
	gGestures = new IGesture*[gGestureCount];
	std::cout << "Gesture count: " << gGestureCount << std::endl;
	hr = gGestureDatabase->get_AvailableGestures(gGestureCount, gGestures);
	if (FAILED(hr)) {
		error(13);
		return false;
	}
	/*************************************/
	/*******   To be continued  *********/

	/*/ Get Frame Reader
	hr = gVgbFrameReader->get_VisualGestureBuilderFrameSource(&vgbFrameSource);
	if (FAILED(hr)) {
		error(14);
		success = false;
	}*/

	// Print gesture name
	/************************************/
	for (int i = 0; i < gGestureCount; i++) {
		nameOfGesture[i] = gestureName(gGestures[i]);
		std::cout << nameOfGesture[i].c_str() << std::endl;
	}
	/************************************/
	/*wchar_t name[10];
	gestures[0]->get_Name(10, name);
	std::cout << "Count: " << gestureCount;
	std::wcout << " Name: " << name << std::endl;
	*/
	// Add gesture to the source
	//for (int i = 0; i < gGestureCount; i++) {
		hr = gVgbFrameSource->AddGestures(gGestureCount, gGestures);
		if (FAILED(hr)) {

			error(15);
			return false;
		}
	//}

	// Enable Gestures
	for (int i = 0; i < gGestureCount; i++) {
		hr = gVgbFrameSource->SetIsEnabled(gGestures[i], TRUE);
		if (FAILED(hr)) {
			error(16);
			return false;
		}
	}


	return true;
}

void drawPixelBuffer(SDL_Texture *texture, SDL_Renderer *renderer, Uint32 *pixelBuffer) {
	void* pixels;
	int pitch;

	// Copy pixel buffer to a texture
	SDL_LockTexture(texture, nullptr, &pixels, &pitch);
	memcpy(pixels, pixelBuffer, WINDOW_WIDTH * WINDOW_HEIGHT * 4);
	SDL_UnlockTexture(texture);

	// Set Viewport
	SDL_RenderSetViewport(renderer, &windowViewport);

	// Copy texture
	SDL_RenderCopy(renderer, texture, nullptr, nullptr);
	//SDL_RenderPresent(renderer);
}

void drawVideoBuffer(SDL_Texture *texture, SDL_Renderer *renderer, unsigned char *videoBuffer) {
	void* pixels;
	int pitch;

	// If image is received then copy it
	if (videoImageReady) {
		// Copy pixel buffer to a texture
		SDL_LockTexture(texture, nullptr, &pixels, &pitch);
		memcpy(pixels, videoBuffer, VIDEO_WIDTH * VIDEO_HEIGHT * 3);
		SDL_UnlockTexture(texture);
		askForImage = true;
	}

	// Set Viewport
	SDL_RenderSetViewport(renderer, &videoViewport);

	// Copy texture
	SDL_RenderCopy(renderer, texture, nullptr, nullptr);
	//SDL_RenderPresent(renderer);
}

void drawHandPosition(SDL_Texture *texture, SDL_Renderer *renderer, ColorSpacePoint left, ColorSpacePoint right) {
	// Set Viewport
	//SDL_RenderSetViewport(renderer, &windowViewport);

	// Color the rectangles
	SDL_SetRenderDrawColor(renderer, 0x00, 0xff, 0x00, 0x55);

	// Create rectangles 
	if (left.X >= 0 && left.X < 1920 && left.Y >= 0 && left.Y < 1080) {
		SDL_Rect leftRect = { left.X, left.Y, 30, 30 };
		SDL_RenderFillRect(renderer, &leftRect);
	}
	if (left.X >= 0 && left.X < 1920 && left.Y >= 0 && left.Y < 1080) {
		SDL_Rect rightRect = { right.X, right.Y, 30, 30 };
		SDL_RenderFillRect(renderer, &rightRect);
	}
}

bool winsockInit() {
	// Socket Init
	WSAData WinSockData;
	WORD DLLVersion = MAKEWORD(2, 1);
	if (WSAStartup(DLLVersion, &WinSockData) != 0) {
		std::cout << "Winsock startup failed..." << std::endl;
		WSACleanup();
		return false;
	}
	else {
		std::cout << "Winsock startup successful" << std::endl;
		return true;
	}
}
 

bool sdlInit() {

	// SDL init
	SDL_Init(SDL_INIT_VIDEO);

	//Create window
	window = SDL_CreateWindow("Kinect Feed", 0, 0,
		WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE);
	if (window == nullptr) {
		error(-1);
		return false;
	}

	/*******************************************************************/
	SDL_SetWindowSize(window, 1366, 768);
	/******************************************************************/

	//Create renderer
	renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
	if (renderer == nullptr) {
		error(-2);
		return false;;
	}

	//Create textures
	windowTexture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_ARGB8888,
		SDL_TEXTUREACCESS_STREAMING, WINDOW_WIDTH, WINDOW_HEIGHT);
	if (windowTexture == nullptr) {
		error(-3);
		return false;
	}
	videoTexture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_BGR24,
		SDL_TEXTUREACCESS_STREAMING, VIDEO_WIDTH, VIDEO_HEIGHT);
	if (windowTexture == nullptr) {
		error(-3);
		return false;
	}

	// Viewport Init
	windowViewport.x = 0;
	windowViewport.y = 0;
	windowViewport.w = WINDOW_WIDTH;
	windowViewport.h = WINDOW_HEIGHT;

	videoViewport.x = 1366 - VIDEO_WIDTH * 3;
	videoViewport.y = 768 - VIDEO_HEIGHT * 3;
	videoViewport.w = VIDEO_WIDTH * 3;
	videoViewport.h = VIDEO_HEIGHT * 3;

	// Init pixel buffer
	pixelBuffer = new Uint32[WINDOW_WIDTH * WINDOW_HEIGHT];
	memset(pixelBuffer, 0, WINDOW_WIDTH * WINDOW_HEIGHT * 4);
	drawPixelBuffer(windowTexture, renderer, pixelBuffer);

	// Init video buffer
	videoBuffer = new unsigned char[VIDEO_WIDTH * VIDEO_HEIGHT * 3];
	memset(videoBuffer, 0x52, VIDEO_WIDTH * VIDEO_HEIGHT * 3);

	// Resize window
	//SDL_SetWindowSize(window, 1280, 720);

	return true;
}

int main(int argc, char* argv[]) {
	HRESULT hr;
	// Kinect Initialization 
	if (!kinectInit()) {
		std::cout << "Kinect could not be initialized!" << std::endl;
		system("pause");
		return 0;
	}

	// SDL Initialization
	if (!sdlInit()) {
		std::cout << "Sdl could not be initialized!" << std::endl;
		system("pause");
		return 0;
	}

	// Socket Initialization
	if (!winsockInit()) {
		std::cout << "WinSock could not be initialized!" << std::endl;
	}

	// Create thread for socket connection
	SDL_Thread* socketThreadID = SDL_CreateThread(socketThread, "SocketThread", NULL);

	// Create thread for video feed
	SDL_Thread* videoThreadID = SDL_CreateThread(videoThread, "VideoThread", NULL);

	// Main loop
	std::string command = "";
	bool newCommand = false;
	bool quit = false;
	SDL_Event ev;
	int countedFrames = 0;
	Uint32 startTime, frameTicks, totalTix;
	const int ticksPerFrame = 1000 / 30;
	IColorFrame* colorFrame = nullptr;
	IBodyFrame* bodyFrame = nullptr;
	IBody* bodies[BODY_COUNT] = { 0 };
	IBody* body = nullptr;
	IVisualGestureBuilderFrame *vgbFrame = nullptr;
	BOOLEAN tracked = false;
	Uint64 trackingId = 0;
	Joint joints[JointType_Count];
	CameraSpacePoint rightHandPos, leftHandPos;
	ColorSpacePoint rightColorPoint, leftColorPoint;
	while (!quit) {
		// When this frame starts
		startTime = SDL_GetTicks();
		
		countedFrames++;

		// Check events for when to quit
		while (SDL_PollEvent(&ev)) {
			switch (ev.type) {
			// If X is pressed
			case SDL_QUIT:
				quit = true;
				break;
			// If Esc is pressed
			case SDL_KEYDOWN:
				if (ev.key.keysym.scancode == SDL_SCANCODE_ESCAPE)
					quit = true;
				else if (ev.key.keysym.scancode == SDL_SCANCODE_UP)
					send(socketConnection, "||||forward", 11, NULL);
				else if (ev.key.keysym.scancode == SDL_SCANCODE_DOWN)
					send(socketConnection, "||||backwards", 13, NULL);
				else if (ev.key.keysym.scancode == SDL_SCANCODE_LEFT)
					send(socketConnection, "||||left", 8, NULL);
				else if (ev.key.keysym.scancode == SDL_SCANCODE_RIGHT)
					send(socketConnection, "||||right", 9, NULL);
				else if (ev.key.keysym.scancode == SDL_SCANCODE_S)
					send(socketConnection, "Stop", 4, NULL);
				break;
			default:
				break;
			}
		}

		// Acquire Latest Frame
		hr = gColorFrameReader->AcquireLatestFrame(&colorFrame);
		if (SUCCEEDED(hr)) {
			// Copy to pixelBuffer
			hr = colorFrame->CopyConvertedFrameDataToArray(1920 * 1080 * 4, (BYTE*)pixelBuffer, ColorImageFormat_Bgra);
		}
		SafeRelease(colorFrame);

		// Acquire Latest Body Frame
		hr = gBodyFrameReader->AcquireLatestFrame(&bodyFrame);
		if (SUCCEEDED(hr)) {
			// Get number of bodies
			hr = bodyFrame->GetAndRefreshBodyData(_countof(bodies), bodies);
			if (SUCCEEDED(hr)) {
				// If a tracked body exists then use it
				if(tracked && body != nullptr)
					hr = body->get_IsTracked(&tracked);
				// Else search for a new body
				else{
					for (int i = 0; i < BODY_COUNT; i++) {
						bodies[i]->get_IsTracked(&tracked);
						if (tracked) {
							body = bodies[i];
							body->get_TrackingId(&trackingId);
							gVgbFrameSource->put_TrackingId(trackingId);
							break;
						}
					}
				}
				if (tracked) {
					// Get the joints
					hr = body->GetJoints(_countof(joints), joints);
					if (SUCCEEDED(hr)) {
						for (int j = 0; j < _countof(joints); j++) {
							// Get position of right and left hand
							if (joints[j].JointType == JointType_HandRight) {
								rightHandPos = joints[j].Position;
								gCoordinateMapper->MapCameraPointToColorSpace(rightHandPos, &rightColorPoint);
							}
							else if (joints[j].JointType == JointType_HandLeft) {
								leftHandPos = joints[j].Position;
								gCoordinateMapper->MapCameraPointToColorSpace(leftHandPos, &leftColorPoint);
							}
						}
					}							
				}
				// Get vgb Frame
				hr = gVgbFrameReader->CalculateAndAcquireLatestFrame(&vgbFrame);
				if (SUCCEEDED(hr)) {
					// Check if frame is valid
					BOOLEAN validId = false;
					hr = vgbFrame->get_IsTrackingIdValid(&validId);
					if (SUCCEEDED(hr) && validId) {
						// Check which gesture is detected
						for (int i = 0; i < gGestureCount; i++) {
							// Check if gesture is detected
							IDiscreteGestureResult *vgbResult = nullptr;
							hr = vgbFrame->get_DiscreteGestureResult(gGestures[i], &vgbResult);
							if (SUCCEEDED(hr)) {
								BOOLEAN vgbDetected = false;
								hr = vgbResult->get_Detected(&vgbDetected);
								if (SUCCEEDED(hr) && vgbDetected) {
									float confidence = 0;
									vgbResult->get_Confidence(&confidence);
									if (confidence >= 0.4) {
										if (command != gestureName(gGestures[i])) {
											command = gestureName(gGestures[i]);
											newCommand = true;
											std::cout << command.c_str() << " detected! Confidence: " << confidence << std::endl;
										} else {
											newCommand = false;
										}
									}
								}
							}
						}
					}
				}
			}
		}
		SafeRelease(bodyFrame);

		// Send command to robot
		if (newCommand && connected) {
			if (command == "Back")
				send(socketConnection, "||||backwards", 13, NULL);
			else if(command == "Front")
				send(socketConnection, "||||forward", 11, NULL);
			else if (command == "Left")
				send(socketConnection, "||||left", 8, NULL);
			else if (command == "Right")
				send(socketConnection, "||||right", 9, NULL);
			else if (command == "Stop")
				send(socketConnection, "Stop", 4, NULL);
			else if (command == "Terminate")
				quit = true;
			newCommand = false;
		}

		// Draw the current Frame
		drawPixelBuffer(windowTexture, renderer, pixelBuffer);

		// Draw hands on texture
		drawHandPosition(windowTexture, renderer, leftColorPoint, rightColorPoint);

		// Draw received video
		if(connected)
			drawVideoBuffer(videoTexture, renderer, videoBuffer);

		// Present the texture on screen
		SDL_RenderPresent(renderer);

		
		// Cap frame rate to 30 fps
		/*frameTicks = SDL_GetTicks() - startTime;
		totalTix += frameTicks;
		if (totalTix >= 1000) {
			totalTix = 0;
			printf("Frames this second: %d\n", countedFrames);
			countedFrames = 0;
		}*/
	

	}

	// Close socket
	const char QUITVIDEO[8] = "Quit";
	send(socketConnection, QUITVIDEO, 4, NULL);
	closesocket(socketConnection);

	// SDL Clean up
	SDL_DestroyWindow(window);
	window = nullptr;
	SDL_DestroyRenderer(renderer);
	renderer = nullptr;
	SDL_DestroyTexture(windowTexture);
	windowTexture = nullptr;
	SDL_Quit;

	// Kinect Cleanup
	SafeRelease(gColorFrameReader);

	system("pause");
	return 0;
}