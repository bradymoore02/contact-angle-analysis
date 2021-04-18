# Contact Angle Analysis
Take raw image files of a drop on a surface and analyze the contact angles
### Quick Start (MacOS)
1. Download FIJI
2.

### Procedure (MacOS)
##### 1. Prepare Images
1. Open folder with images in Finder
2. Select all (⌘A)
3. Open with Preview (⌘O)
4. Use mouse to select only the area containing the drop
5. Crop the image (⌘K)
6. Go to next image (down arrow key)
7. Repeat steps 4 and 5 for each image
##### 2. ImageJ
1. Open FIJI
2. Drag the first cropped image file from finder into the lower bar in FIJI.
![](/examples/FIJI_toolbar)
3. Start typing "Contact Angle" into the FIJI search bar
4. Hit enter to open the Contact Angle plugin
5. On the image, click the first point where the drop meets the stage. This should place a small colored cross at the location that you clicked.
6. Place another cross at the other location where the drop meets the stage.
7. Starting from where the last cross was placed, place about 10 more crosses along the edge of the drop concentrating them mostly in the areas just above where the drop contacts the stage.
8. Click the button with the page icon in the ImageJ toolbar.
9. Select "Manual Points Procedure"
10. Open the next image in FIJI(⌘⇧O)
11. Repeat steps 3 through 10 until this has been done for each image.
12. Click on the results file and save as "Results.csv" in the same directory as the contact-angle-analysis folder.

##### 3. Analysis
1. Open a terminal and navigate to the Contact Angle Analysis directory.
2. Run the post_processing.py file by typing the following into the command line:
```
python3 post_processing.py
```
3. Two csv files are created as output. Output_byDrop.csv organizes the data by drop and Output_byImage.csv organizes the data by image.
