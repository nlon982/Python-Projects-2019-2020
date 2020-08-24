I am taking this course which provides 3rd party lecture videos (found on Youtube). Something that would improve my life is if I could have access to these slides to take notes on. So I set out to make a tool that, when given a video (which goes through a powerpoint), gives you all the slides.

I have the script at every x amount of frames (the bigger x is, the longer it takes), and compares the current frame to the next frame; if the slides are different enough, it saves that frame. I.e. if there is big enough change in a frame, you get that frame. With slides which have transitions (i.e. the content comes in incrementally), you'd get all of the different versions of every single slide. So I ran a second pass to go through those slides, and just take the final version of every slide - that is, logically, the slide where there is a massive difference between the current frame in the next frame.

The above logic is crass (I don't think the second pass is necessary - that could be done in the first pass), but this is something I put together as quick as possible.

So the final outcome is: you run this Python file in a folder and it takes every '.mp4' item, and obtains the slides from them - and saves them out.
