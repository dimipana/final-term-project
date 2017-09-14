package iristk.app.guess;

import java.util.List;
import java.io.File;
import iristk.xml.XmlMarshaller.XMLLocation;
import iristk.system.Event;
import iristk.flow.*;
import iristk.util.Record;
import static iristk.util.Converters.*;
import static iristk.flow.State.*;

public class GuessFlow extends iristk.flow.Flow {

	private Integer action;
	private String motion;

	private void initVariables() {
	}

	public Integer getAction() {
		return this.action;
	}

	public void setAction(Integer value) {
		this.action = value;
	}

	public String getMotion() {
		return this.motion;
	}

	public void setMotion(String value) {
		this.motion = value;
	}

	@Override
	public Object getVariable(String name) {
		if (name.equals("action")) return this.action;
		if (name.equals("motion")) return this.motion;
		return null;
	}


	public GuessFlow() {
		initVariables();
	}

	@Override
	protected State getInitialState() {return new Start();}

	public static String[] getPublicStates() {
		return new String[] {};
	}

	private class Start extends State {

		final State currentState = this;


		@Override
		public void setFlowThread(FlowRunner.FlowThread flowThread) {
			super.setFlowThread(flowThread);
		}

		@Override
		public void onentry() {
			int eventResult;
			Event event = new Event("state.enter");
			EXECUTION: {
				int count = getCount(195600860) + 1;
				incrCount(195600860);
				iristk.flow.DialogFlow.say state0 = new iristk.flow.DialogFlow.say();
				state0.setText("Command the robot to take an action. You can select to move it onwards, backwards, left, or right.");
				if (!flowThread.callState(state0, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 10, 12)))) {
					eventResult = EVENT_ABORTED;
					break EXECUTION;
				}
				Guess state1 = new Guess();
				flowThread.gotoState(state1, currentState, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 13, 25)));
				eventResult = EVENT_ABORTED;
				break EXECUTION;
			}
		}

		@Override
		public int onFlowEvent(Event event) {
			int eventResult;
			int count;
			eventResult = super.onFlowEvent(event);
			if (eventResult != EVENT_IGNORED) return eventResult;
			eventResult = callerHandlers(event);
			if (eventResult != EVENT_IGNORED) return eventResult;
			return EVENT_IGNORED;
		}

	}


	private class Guess extends Dialog {

		final State currentState = this;


		@Override
		public void setFlowThread(FlowRunner.FlowThread flowThread) {
			super.setFlowThread(flowThread);
		}

		@Override
		public void onentry() {
			int eventResult;
			Event event = new Event("state.enter");
			EXECUTION: {
				int count = getCount(1973336893) + 1;
				incrCount(1973336893);
				iristk.flow.DialogFlow.listen state2 = new iristk.flow.DialogFlow.listen();
				if (!flowThread.callState(state2, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 18, 12)))) {
					eventResult = EVENT_ABORTED;
					break EXECUTION;
				}
			}
		}

		@Override
		public int onFlowEvent(Event event) {
			int eventResult;
			int count;
			count = getCount(1212899836) + 1;
			MyClient clientmes = new MyClient();
			if (event.triggers("sense.user.speak")) {
				if (event.has("sem:action")) {
					incrCount(1212899836);
					eventResult = EVENT_CONSUMED;
					EXECUTION: {
						if (asInteger(event.get("sem:action")) == 1) {
							iristk.flow.DialogFlow.say state3 = new iristk.flow.DialogFlow.say();
							state3.setText("You told the robot to move forward.");
							if (!flowThread.callState(state3, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 23, 48)))) {
								eventResult = EVENT_ABORTED;
								break EXECUTION;
							}
							motion="forward";
							clientmes.connect(motion);
							
							flowThread.reentryState(this, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 27, 15)));
							eventResult = EVENT_ABORTED;
							break EXECUTION;
						} else if (asInteger(event.get("sem:action"))==2) {
							iristk.flow.DialogFlow.say state4 = new iristk.flow.DialogFlow.say();
							state4.setText("You told the robot to move backward.");
							if (!flowThread.callState(state4, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 23, 48)))) {
								eventResult = EVENT_ABORTED;
								break EXECUTION;
							}
							motion="backwards";
							clientmes.connect(motion);
							flowThread.reentryState(this, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 32, 15)));
							eventResult = EVENT_ABORTED;
							break EXECUTION;
						} else if (asInteger(event.get("sem:action"))==3) {
							iristk.flow.DialogFlow.say state5 = new iristk.flow.DialogFlow.say();
							state5.setText("You told the robot to turn left.");
							if (!flowThread.callState(state5, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 23, 48)))) {
								eventResult = EVENT_ABORTED;
								break EXECUTION;
							}
							motion="left";
							clientmes.connect(motion);
							flowThread.reentryState(this, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 37, 15)));
							eventResult = EVENT_ABORTED;
							break EXECUTION;
						} else if (asInteger(event.get("sem:action"))==4) {
							iristk.flow.DialogFlow.say state6 = new iristk.flow.DialogFlow.say();
							state6.setText("You told the robot to turn right.");
							if (!flowThread.callState(state6, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 23, 48)))) {
								eventResult = EVENT_ABORTED;
								break EXECUTION;
							}
							motion="right";
							clientmes.connect(motion);
							flowThread.reentryState(this, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 42, 15)));
							eventResult = EVENT_ABORTED;
							break EXECUTION;
						}
					}
					if (eventResult != EVENT_IGNORED) return eventResult;
				}
			}
			eventResult = super.onFlowEvent(event);
			if (eventResult != EVENT_IGNORED) return eventResult;
			eventResult = callerHandlers(event);
			if (eventResult != EVENT_IGNORED) return eventResult;
			return EVENT_IGNORED;
		}

	}


	private class CheckAgain extends Dialog {

		final State currentState = this;


		@Override
		public void setFlowThread(FlowRunner.FlowThread flowThread) {
			super.setFlowThread(flowThread);
		}

		@Override
		public void onentry() {
			int eventResult;
			Event event = new Event("state.enter");
			EXECUTION: {
				int count = getCount(250075633) + 1;
				incrCount(250075633);
				iristk.flow.DialogFlow.say state7 = new iristk.flow.DialogFlow.say();
				state7.setText("Do you want to play again?");
				if (!flowThread.callState(state7, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 48, 12)))) {
					eventResult = EVENT_ABORTED;
					break EXECUTION;
				}
				iristk.flow.DialogFlow.listen state8 = new iristk.flow.DialogFlow.listen();
				if (!flowThread.callState(state8, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 48, 12)))) {
					eventResult = EVENT_ABORTED;
					break EXECUTION;
				}
			}
		}

		@Override
		public int onFlowEvent(Event event) {
			int eventResult;
			int count;
			count = getCount(358699161) + 1;
			if (event.triggers("sense.user.speak")) {
				if (event.has("sem:yes")) {
					incrCount(358699161);
					eventResult = EVENT_CONSUMED;
					EXECUTION: {
						iristk.flow.DialogFlow.say state9 = new iristk.flow.DialogFlow.say();
						state9.setText("Okay, let's play again.");
						if (!flowThread.callState(state9, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 52, 58)))) {
							eventResult = EVENT_ABORTED;
							break EXECUTION;
						}
						Start state10 = new Start();
						flowThread.gotoState(state10, currentState, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 54, 25)));
						eventResult = EVENT_ABORTED;
						break EXECUTION;
					}
					if (eventResult != EVENT_IGNORED) return eventResult;
				}
			}
			count = getCount(914424520) + 1;
			if (event.triggers("sense.user.speak")) {
				if (event.has("sem:no")) {
					incrCount(914424520);
					eventResult = EVENT_CONSUMED;
					EXECUTION: {
						iristk.flow.DialogFlow.say state11 = new iristk.flow.DialogFlow.say();
						state11.setText("Okay, goodbye");
						if (!flowThread.callState(state11, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 56, 57)))) {
							eventResult = EVENT_ABORTED;
							break EXECUTION;
						}
						System.exit(0);
					}
					if (eventResult != EVENT_IGNORED) return eventResult;
				}
			}
			eventResult = super.onFlowEvent(event);
			if (eventResult != EVENT_IGNORED) return eventResult;
			eventResult = callerHandlers(event);
			if (eventResult != EVENT_IGNORED) return eventResult;
			return EVENT_IGNORED;
		}

	}


	private class Dialog extends State {

		final State currentState = this;


		@Override
		public void setFlowThread(FlowRunner.FlowThread flowThread) {
			super.setFlowThread(flowThread);
		}

		@Override
		public void onentry() {
			int eventResult;
			Event event = new Event("state.enter");
		}

		@Override
		public int onFlowEvent(Event event) {
			int eventResult;
			int count;
			count = getCount(2143192188) + 1;
			if (event.triggers("sense.user.silence")) {
				incrCount(2143192188);
				eventResult = EVENT_CONSUMED;
				EXECUTION: {
					iristk.flow.DialogFlow.say state12 = new iristk.flow.DialogFlow.say();
					state12.setText("I am sorry, I didn't hear anything.");
					if (!flowThread.callState(state12, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 63, 38)))) {
						eventResult = EVENT_ABORTED;
						break EXECUTION;
					}
					flowThread.reentryState(this, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 65, 14)));
					eventResult = EVENT_ABORTED;
					break EXECUTION;
				}
				if (eventResult != EVENT_IGNORED) return eventResult;
			}
			count = getCount(204349222) + 1;
			if (event.triggers("sense.user.speak")) {
				incrCount(204349222);
				eventResult = EVENT_CONSUMED;
				EXECUTION: {
					iristk.flow.DialogFlow.say state13 = new iristk.flow.DialogFlow.say();
					state13.setText("I am sorry, I didn't get that.");
					if (!flowThread.callState(state13, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 67, 36)))) {
						eventResult = EVENT_ABORTED;
						break EXECUTION;
					}
					flowThread.reentryState(this, new FlowEventInfo(currentState, event, new XMLLocation(new File("C:\\Users\\Idleflair\\IrisTK\\app\\guess\\src\\iristk\\app\\guess\\GuessFlow.xml"), 69, 14)));
					eventResult = EVENT_ABORTED;
					break EXECUTION;
				}
				if (eventResult != EVENT_IGNORED) return eventResult;
			}
			eventResult = super.onFlowEvent(event);
			if (eventResult != EVENT_IGNORED) return eventResult;
			eventResult = callerHandlers(event);
			if (eventResult != EVENT_IGNORED) return eventResult;
			return EVENT_IGNORED;
		}

	}


}
