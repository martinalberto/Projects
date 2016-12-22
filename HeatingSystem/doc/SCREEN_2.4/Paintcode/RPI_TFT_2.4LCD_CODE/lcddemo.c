#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "lcd.h"
#include "SFont.h"

extern void Pant(unsigned int color);
extern void SetPinNU(short P0,short P1,short P2,short P3,short P4,short P5,short P6,short P7,
			short Prs,short Pcs,short Pwr,short Prst,short Pdout,short Pirq,short Pdin,short Pclk);
int main (void)
{
	
	int buf[318];
	int x, x2;
	int y, y2;
	int r;
	int i;
  	wiringPiSetup();									//设置树莓派GPIO
  	SetPinNU(0,1,2,3,4,5,6,7,9,11,8,16,13,10,12,14);	//设置引脚（参考树莓派GPIO映射图）
	SetLCDSize(LCD_24);									//设置使用的LCD尺寸	
	LCDInit();											//初始化LCD	
  	Touch_Init();										//初始化触摸
	setFont(8,12,32);									//设置字体为8x12
  	setColor(0x07e0);									//设置字体颜色
  	setBackColor(0xf800);								//设置背景颜色	

	printf("Init is ok!\n");
	
 while(1) 
 {
   	clrScr();
//	printNumI(1000000000,10,40,10,0);
//	printNumF(5.8964,4,20,60,'.',6,' ');
//  delay(5000);
   setColorRGB(255, 0, 0);
   fillRect(0, 0, 319, 13);
   setColorRGB(64, 64, 64);
   fillRect(0, 226, 319, 239);
   setColorRGB(255, 255, 255);
   setBackColorRGB(255, 0, 0);
   print("* Universal Color TFT Display Library *", CENTER,1,0);
   printf("* Universal Color TFT Display Library *");
   setBackColorRGB(64, 64, 64);
   setColorRGB(255,255,0);
   print("<http://electronics.henningkarlsen.com>", CENTER,227,0);
   printf("* henningkarlsen *");
   setColorRGB(0, 0, 255);
   drawRect(0, 14,319,225);

   setColorRGB(0, 0, 255);
   setBackColorRGB(0, 0, 0);
   drawLine(159, 15, 159, 224);
   drawLine(1, 119, 318, 119);
  for (i=9; i<310; i+=10)
     drawLine(i, 117, i, 121);
  for (i=19; i<220; i+=10)
     drawLine(157, i, 161, i);

   setColorRGB(0,255,255);
   print("Sin", 5, 15,0);
  for (i=1; i<318; i++)
  {
     drawPixel(i,119+(sin(((i*1.13)*3.14)/180)*95));
  }
  
   setColorRGB(255,0,0);
   print("Cos", 5, 27,0);
  for (i=1; i<318; i++)
  {
     drawPixel(i,119+(cos(((i*1.13)*3.14)/180)*95));
  }

   setColorRGB(255,255,0);
   print("Tan", 5, 39,0);
  for (i=1; i<318; i++)
  {
     drawPixel(i,119+(tan(((i*1.13)*3.14)/180)));
  }

  delay(2000);

   setColorRGB(0,0,0);
   fillRect(1,15,318,224);
   setColorRGB(0, 0, 255);
   setBackColorRGB(0, 0, 0);
   drawLine(159, 15, 159, 224);
   drawLine(1, 119, 318, 119);

  x=1;
  for (i=1; i<(318*20); i++) 
  {
    x++;
    if (x==319)
      x=1;
    if (i>319)
    {
      if ((x==159)||(buf[x-1]==119))
         setColorRGB(0,0,255);
      else
         setColorRGB(0,0,0);
       drawPixel(x,buf[x-1]);
    }
     setColorRGB(0,255,255);
    y=119+(sin(((i*1.1)*3.14)/180)*(90-(i / 100)));
     drawPixel(x,y);
    buf[x-1]=y;
  }

  delay(2000);
  
   setColorRGB(0,0,0);
   fillRect(1,15,318,224);

  for (i=1; i<6; i++)
  {
    switch (i)
    {
      case 1:
         setColorRGB(255,0,255);
        break;
      case 2:
         setColorRGB(255,0,0);
        break;
      case 3:
         setColorRGB(0,255,0);
        break;
      case 4:
         setColorRGB(0,0,255);
        break;
      case 5:
         setColorRGB(255,255,0);
        break;
    }
     fillRect(70+(i*20), 30+(i*20), 130+(i*20), 90+(i*20));
  }

  delay(2000);
  
   setColorRGB(0,0,0);
   fillRect(1,15,318,224);

  for (i=1; i<6; i++)
  {
    switch (i)
    {
      case 1:
         setColorRGB(255,0,255);
        break;
      case 2:
         setColorRGB(255,0,0);
        break;
      case 3:
         setColorRGB(0,255,0);
        break;
      case 4:
         setColorRGB(0,0,255);
        break;
      case 5:
         setColorRGB(255,255,0);
        break;
    }
     fillRoundRect(190-(i*20), 30+(i*20), 250-(i*20), 90+(i*20));
  }
  
  delay(2000);
  
   setColorRGB(0,0,0);
   fillRect(1,15,318,224);

  for (i=1; i<6; i++)
  {
    switch (i)
    {
      case 1:
         setColorRGB(255,0,255);
        break;
      case 2:
         setColorRGB(255,0,0);
        break;
      case 3:
         setColorRGB(0,255,0);
        break;
      case 4:
         setColorRGB(0,0,255);
        break;
      case 5:
         setColorRGB(255,255,0);
        break;
    }
     fillCircle(100+(i*20),60+(i*20), 30);
  }

  delay(2000);

   setColorRGB(0,0,0);
   fillRect(1,15,318,224);

// Draw some lines in a pattern
   setColorRGB(255,0,0);
  for (i=15; i<224; i+=5)
  {
     drawLine(1, i, (i*1.44)-10, 224);
  }
   setColorRGB(255,0,0);
  for (i=224; i>15; i-=5)
  {
     drawLine(318, i, (i*1.44)-11, 15);
  }
   setColorRGB(0,255,255);
  for (i=224; i>15; i-=5)
  {
     drawLine(1, i, 331-(i*1.44), 15);
  }
   setColorRGB(0,255,255);
  for (i=15; i<224; i+=5)
  {
     drawLine(318, i, 330-(i*1.44), 224);
  }

  delay(2000);

   setColorRGB(0,0,0);
   fillRect(1,15,318,224);

// Draw some random circle
   fillScrRGB(0, 0, 255);
   setColorRGB(255, 0, 0);
   fillRoundRect(80, 70, 239, 169);

   setColorRGB(255, 255, 255);
   setBackColorRGB(255, 0, 0);
   print("That's it!", CENTER, 93,0);
   print("Restarting in a", CENTER, 119,0);
   print("few seconds...", CENTER, 142,0);

   setColorRGB(0, 255, 0);
   setBackColorRGB(0, 0, 255);
   print("Runtime: (msecs)", CENTER, 210,0);
   printNumI(millis(), CENTER, 225,0,0);

//  delay (10000);
    delay (5000);
	if(Touch_DataAvailable)
	{
		Touch_Read();
		x=Touch_GetX();
		y=Touch_GetY();
		printf("%d,%d\n",x,y);
	}
  }

}
