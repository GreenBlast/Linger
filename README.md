# Linger
Linger is a trigger to action configurable platform, written in Python

## What does it do?

It runs, where you run it, and waits for the given triggers to occur, when something like that happens, the trigger would call the actions associated with it.

## What do you use it for?
Right now, I use it to start my Air conditioner few minutes before getting to home using [broadlink RMPro](http://www.ibroadlink.com/rmPro/), to starts [ispy](https://www.ispyconnect.com) on a certain computer, and to start several applications on my Raspberry pi without getting out of my chair. And I intend to use it for various home automation projects in the future (As it more versatile than out of the box solutions, if you know how to program)


## Who should use this?
Linger is not intended to work for everyone right out of the box. The main idea when I writed it is to provide a nice framework to do repetitious Triggers->Actions for myself. Probably when you want it to do something, you should write your own Trigger, Actions, and Adapters to do the job. Then, you are welcome to add them to the collection so that everyone could enjoy them.


## "Your code is bad and you should feel bad!"
_Or: "I read your code, and there is a problem/mistake/your design is wrong_

Well, Linger is a side project I'm working on, and while working on it, I wanted results, and I wanted the work done fast. So I cut some corners, and did some of the things the easy way instead of the right way. As well as I left some things out. You are more than welcome to add suggestions, add your code, or just message me how it was helpful for you

## How?

Linger is seperated to 3 major item types: Triggers, Actions and Adapters.
Triggers, are conditions that when met would call the actions associated with them.
Actions, are pieces of code that would be called by the triggers to do stuff.
Adapters, are pieces of code that do stuff, they are seprated because they are here to be used by triggers, actions, and adapters.

## What Triggers, Actions, and Adapters are there?

### Triggers:

* DirWatchTrigger.py - Watches a directory for changes and calls it's actions when there is one
* FileDeleteTrigger.py - Creates a file, and triggers when it's deleted. Creating the file again afterwards
* NewMailFilterByCommandTrigger.py – Wait for a mail with a given subject to arrive, and calls the action with the label in the mail
* OnStartTrigger.py – Calls its actions 5 seconds after Linger is up
* PeriodicalTrigger.py – Calls its actions every given interval in seconds, using Linger scheduler
* ThreadedPeriodicalTrigger.py – Creates a thread that calls an action every given interval in seconds
* PeriodicalHumanlikeTrigger.py - Does actions periodically, but adds a random interval and not acting between given sleep times
* TelegramFilterByCommandTrigger.py - Let's you give commands to a telegram bot to engage the given actions associated with the trigger
* MQTTMessageFilterByCommandTrigger.py - Triggers by a message received from an MQTT broker to engage given action associated with the trigger
* MultipleLingersTelegramFilterByCommandTrigger - A telegram trigger that enables controlling more than one Linger instances (by two stages, send an MQTT message that gets in response a list of available commands of an MQTT trigger in another Linger)
### Actions

* GetGrabAndSendMailAction.py – Takes a snapshot using an [ispy](https://www.ispyconnect.com) adapter, and sending it to a Mail recipient
* IspyStartAction.py – Starts [ispy](https://www.ispyconnect.com)
* IspyStopAction.py – Stops [ispy](https://www.ispyconnect.com)
* LogFileChangeAction.py – Prints to the log a given file change
* RestartLingerAction.py – Restarts Linger
* ShutdownLingerAction.py – Shutting down Linger
* StartProcessAction.py – Starts a process using process adapter
* StopProcessAction.py – Stops process using process adapter
* StopProcessAndChildrenAction.py – Stops all children of a process and then stops the process using process adapter
* TestLogAction.py – Prints a given line to the log
* StartACIfTempAction.py - Starts the Air conditioner by using RMBridgeAdapter if current temperature is above the given min temperature
* StopACAction.py - Stops the Air conditioner by using RMBridgeAdapter
* ToggleACStateAction.py - Toggles the Air conditioner in the RMBridgeAdapter
* ShellCommandAction.py - Calls a command to be executed (using subprocess.call)
* MQTTPublishAction.py - Publishes a message on an MQTT broker
* TriggerLabelsSendAction.py - Sends a list of labels of actions associated with a trigger, to be used with MultipleLingersTelegramFilterByCommandTrigger
### Adapters

* DirWatchAdapter.py - Adapter that uses python-watchdog to watch over directory changes, most of the time there should be only one active, because it can handle more than one directory for each instance
* GMailAdapter.py – Adapter that helps to interact with Gmail (Send mails, check periodically for new mails)
* IspyAdapter.py – Adapters to send command to an [Ispy](https://www.ispyconnect.com) server
* LogAdapter.py - Adapter that write lines to the log
* ProcessAdapter.py – Adapter that manages an instance of a process
* RMBridgeAdapter.py - Adapter to communicate with [RMBridge](http://rm-bridge.fun2code.de/) Which sends commands to a [broadlink RMPro](http://www.ibroadlink.com/rmPro/)
* TelegramBotAdapter.py – Adapter that manages a telegram bot using the Telegram bot api and a respective python library. To get auth token create your bot via [BotFather](https://telegram.me/BotFather) in telegram
* TelegramCommunicationAdapter.py – Adapter that manages sending a message to chat via the bot adapter. A registration is needed via the given command.
* MQTTAdapter.py - Adapter which manages MQTT client communication
* MQTTCommunicationAdapter.py - Adapter which manages sending MQTT messagas with a predefined topic