/*

 _____     ______     ______     __     __    
/\  __-.  /\  == \   /\  __ \   /\ \  _ \ \   
\ \ \/\ \ \ \  __<   \ \  __ \  \ \ \/ ".\ \  
 \ \____-  \ \_\ \_\  \ \_\ \_\  \ \__/".~\_\ 
  \/____/   \/_/ /_/   \/_/\/_/   \/_/   \/_/ 
                                              




Disclamer:
You canot save any art (Yet!)
!!!!If the project gets laggy pls press the restart button!!!!

Sometimes Buttons do not work


Sometimes it looks like 2 buttons have been pressed at once, if you are shoure you did not click both at the same time then pls continue to work on your art.

The ereaser tool is 10 pixels bigger than the current selected size.


Created by RaskAttack!


!!!Below is info for me (RaskAttack)!!!



Tool Info:
Ereaser = 0
Pen = 1
Winston = 2
Rectange Pen = 3
Text = 4

> Greater than < less than
*/









var Die = 20;
var Tool = 1;


draw = function() {
    //Toolbar rect
    fill(255, 255, 255);
    rect(330, 0, 70, 400);
      
    // Pen
    if (mouseIsPressed && Tool === 1){
    fill(mouseX, mouseY, 0);
    stroke(mouseX, mouseY, 0);
    
    
    ellipse(mouseX, mouseY, Die, Die);
    }
    //Ereaser
    if (mouseIsPressed && Tool === 0){
        fill(255, 255, 255);
        stroke(255, 255, 255);
        
        ellipse(mouseX, mouseY, Die + 10, Die + 10);
    }
    // Winston Drawer
    if (mouseIsPressed && Tool === 2) {
        image(getImage("creatures/Winston"), mouseX-Die, mouseY-Die, Die, Die);
    }
    //Rectangle Pen
    if (mouseIsPressed && Tool === 3) {
        fill(mouseX, mouseY, 0);
        stroke(mouseX, mouseY, 0);
        
        rect(mouseX, mouseY, Die, Die);
    }
    //Text
    if (mouseIsPressed && Tool ===4) {
        fill(mouseX, mouseY, 0);
        stroke(mouseX, mouseY, 0);
        textSize(Die);
        
        text("Draw!", mouseX, mouseY);
    }
    //X & Y pos
    fill(255, 255, 255);
    stroke(255, 255, 255);
    fill(0, 0, 0);
    textSize(12);
    text(mouseX, 380, 12);
    text(mouseY, 380, 22);
    text("X", 370, 12);
    text("Y", 370, 22);
    //Toolbar
    textSize(15);
    text("Toolbar", 340, 35);
    //Info Scetion
    textSize(13);
    text("Info:", 354, 48);
    //Next Color
    textSize(12);
    text("Next Color", 336, 58);
    fill(mouseX, mouseY, 0);
    rect(331, 62, 66, 20);
    fill(0, 0, 0);
    //Tools Setcion
    textSize(13);
    text("Tools", 345, 99);
    //Ereaser & Pen
    textSize(12);
    rect(335, 110, 60, 20);
    rect(335, 130, 60, 20);
    fill(255, 255, 255);
    text("Ereaser", 343, 124);
    text("Pen", 343, 144);
    fill(0, 0, 0);
    if (mouseX > 335 && mouseX <395 && mouseY > 110 && mouseY < 130 && mouseIsPressed) {
        fill(255, 0, 0);
        rect(335, 110, 60, 20);
        Tool = 0;
    }
     if (mouseX > 335 && mouseX <395 && mouseY > 130 && mouseY < 150 && mouseIsPressed) {
        fill(255, 0, 0);
        rect(335, 130, 60, 20);
        Tool = 1;
    }
    //Winston drawing
    rect(335, 150, 60, 20);
    fill(255, 255, 255);
    text("Winston", 343, 164);
    if (mouseX > 335 && mouseX <395 && mouseY > 150 && mouseY < 170 && mouseIsPressed) {
        fill(255, 0, 0);
        rect(335, 150, 60, 20);
        Tool = 2;
    }
    //Size
    fill(0, 0, 0);
    textSize(13);
    text("Size", 350, 184);
    textSize(12);
    //10
    fill(0, 0, 0);
    rect(335, 200, 20, 20);
    fill(255, 255, 255);
    text("10", 338, 215);
    if (mouseX > 335 && mouseX <395 && mouseY > 200 && mouseY < 220 && mouseIsPressed) {
        fill(255, 0, 0);
        rect(335, 200, 20, 20);
        Die = 10;
    }
    //20
    fill(0, 0, 0);
    rect(369, 200, 20, 20);
    fill(255, 255, 255);
    text("20", 372, 215);
    if (mouseX > 369 && mouseX <389 && mouseY > 200 && mouseY < 220 && mouseIsPressed) {
        fill(255, 0, 0);
        rect(369, 200, 20, 20);
        Die = 20;
    }
    //50
    fill(0, 0, 0);
    rect(353, 225, 20, 20);
    fill(255, 255, 255);
    text("50", 356, 239);
    if (mouseX > 353 && mouseX <378 && mouseY > 225 && mouseY < 245 && mouseIsPressed) {
        fill(255, 0, 0);
        rect(353, 225, 20, 20);
        Die = 50;
    }
    
    //Shapes
    fill(0, 0, 0);
    textSize(13);
    text("Shapes", 342, 269);
    textSize(12);
    //Rectange
    rect(342, 277, 48, 20);
    fill(255, 255, 255);
    text("Rect", 348, 292);
    if (mouseX > 342 && mouseX <362 && mouseY > 277 && mouseY < 324 && mouseIsPressed) {
        fill(255, 0, 0);
        rect(342, 277, 47, 20);
        Tool = 3;
    }
    //Circle
    fill(0, 0, 0);
    rect(342, 298, 47, 20);
    fill(255, 255, 255);
    text("Circle", 348, 312);
    if (mouseX > 342 && mouseX <362 && mouseY > 298 && mouseY < 345 && mouseIsPressed) {
        fill(255, 0, 0);
        rect(342, 298, 47, 20);
        Tool = 1;
    }
    //Line
    fill(0, 0, 0);
    rect(342, 319, 47, 20);
    fill(255, 255, 255);
    text("Text", 350, 333);
    if (mouseX > 342 && mouseX <362 && mouseY > 319 && mouseY < 366 && mouseIsPressed) {
        fill(255, 0, 0);
        rect(342, 319, 47, 20);
        Tool = 4;
    }
};




