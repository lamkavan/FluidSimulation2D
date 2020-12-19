# CSC417: Final Project 2D Fluid Simulation

## Introduction
The following is a solo project completed for CSC417 Physics Based Animations offered at the University of Toronto.
In this final project, a 2D fluid simulation is implemented in Java, a short SIGGRAPH style video is created and
a short SIGGRAPH style paper is written. You will find the details about the code, video and paper below.

## Project Video
To learn more about this project with a short SIGGRAPH style video on Youtube please go [here](https://google.com).
The video provides an introduction to the problem, mentions the important resources used, outlines
the algorithm and finally demonstrates the result. You are encouraged to watch the video before reading the
paper or diving into the code.

## Project Report
You can also read the short SIGGRAPH style paper that explains the algorithm (paper.pdf). Note that the paper 
also uses up three pages for the appendix which is not mandatory to read but offers a more in depth look into 
the algorithm. The appendix is however handwritten (it is very neat), but hopefully that does not 
discourage you from reading it.

## Running the code
Ok, now for the fun part. The following are the instructions for getting the code running and how to
enjoy 2D fluid simulation. Attached to the project submission you will find project.zip and upon
unzipping this you will find get a folder called project and in that folder you will find
a folder called FluidSimulationJava. Looking in that folder you will find a folder called
src which contains all of the Java code written by me that is needed to power this simulation.
Next to the src folder is core.jar which is the dependency required to render the 2D fluid.
To be clear, core.jar is not created by me nor did I write any of the code for core.jar. To
be specific, core.jar is actually [Processing](https://processing.org/) which in this case is
used to render our fluid and is an amazing tool in general.

Alright so how do you actually compile and run the code? Just follow these instructions

1) You will need get your hands on a JDK/SDK. You can get it from [here](https://www.oracle.com/ca-en/java/technologies/javase-jdk15-downloads.html).
You will need the JDK to be able to compile and run the code. You may already have a JDK on your system, but the code
has not been tested on a version of JDK less than 15, but should work with most recent JDKs such as JDK 12 or 13.
Note: I recommend getting the compressed archive since you have more control over it and can simply delete the whole
thing once you are done using it. With that in mind, the remaining instructions will assume you downloaded the compressed archive.

2) After downloading the JDK you need to unzip it and you will get a folder named something like jdk-15.0.1_windows-x64_bin.
Drag and drop this folder and add it next to the src folder (src folder and JDK folder are at the same directory level).

3) Now all you need to do is compile and run the code using javac and java respectively. Open up a terminal and
cd into the src directory. From there you need to issue the following commands.
    ```
    ../jdk-15.0.1_windows-x64_bin/jdk-15.0.1/bin/javac -cp ../core.jar *.java
    ```
    After running that command you will see three .class files created in the src folder. Now you need to run the code.
    ```
    ../jdk-15.0.1_windows-x64_bin/jdk-15.0.1/bin/java -cp ../core.jar:. Main
    ```

    Note that some of the directory/folder names may be different for you. Also note, that the instructions may vary depending on your OS.
    In general, the steps above are very standard for compiling and running java code. If for whatever reason you are not able to get the 
    code running, please contact me by phone 647-282-7786 or by email kavan.lam@mail.utoronto.ca and I will help you out ASAP.