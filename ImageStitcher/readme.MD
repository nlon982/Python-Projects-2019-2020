I took a course called Phil105G. The course had the resources all spread across Canvas - a week's content (called a Module) was on 15 different web pages (and there was 12 weeks of content). I wanted this content offline, and I wanted this content all in one place.

> I made a Python script that went page by page through the content, and would save as screenshot of the entire page. I did this via getting the script to click on a chrome extension which takes full page screenshots (the screenshots were cropped accordingly), and then getting it to find and click the 'next' button at the bottom of the page. Note: I have been unable to find .py file for this, so this isn't on GitHub.

> I made another Python script which then stitched together these images. I found OneNote's image compression meant I couldn't stitch together all of these images (because that'd make a massive image), so I stitched together rows of 5. This is called 'image stitcher.py'.

I have uploaded an example module; the folder 'Module 4' shows screenshots taken with the first script, and the 'temp dir' subdirectory shows the images stitched together by the second script.

This actually turned out to be a project that saved me a lot of time; having the content on OneNote was so helpful. I got it down to being able to learn the content for the week in 3 hours or so (and I pride this on being able to easy navigate through the content thanks to my tool).
