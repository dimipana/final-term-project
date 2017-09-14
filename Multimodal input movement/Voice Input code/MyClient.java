package iristk.app.guess;

import java.io.*;  
import java.net.*; 
public class MyClient {
	int a;
	public MyClient(){}
	
	public static void connect(String a) {  

		try{      
		Socket soc=new Socket("192.168.1.5",2004);  

		DataOutputStream dout=new DataOutputStream(soc.getOutputStream());  
		dout.writeUTF(a);
		dout.flush();
		dout.close();  
		soc.close();
		}catch(Exception e){
		    e.printStackTrace();
		}  
		
	}
}
	

