#include <GxEPD2_3C.h>
#include "GxEPD2_750c_86BF.h"
#include <Fonts/FreeMonoBold9pt7b.h>
#include "Images.h"

GxEPD2_3C<GxEPD2_750c_86BF, GxEPD2_750c_86BF::HEIGHT> display(GxEPD2_750c_86BF(/*CS=D8*/ 5, /*DC=D3*/ 17, /*RST=D4*/ 16, /*BUSY=D2*/ 4));

const char HelloWorld[] = "Hello World!";
const char HelloArduino[] = "Hello Arduino!";

void helloWorld()
{
  display.setFont(&FreeMonoBold9pt7b);
  display.setTextColor(GxEPD_BLACK);
  int16_t tbx, tby;
  uint16_t tbw, tbh;
  display.getTextBounds(HelloWorld, 0, 0, &tbx, &tby, &tbw, &tbh);
  // center the bounding box by transposition of the origin:
  uint16_t x = ((display.width() - tbw) / 2) - tbx;
  uint16_t y = ((display.height() - tbh) / 2) - tby;
  display.setFullWindow();
  display.firstPage();
  do
  {
    display.fillScreen(GxEPD_WHITE);
    display.setCursor(x, y);
    display.print(HelloWorld);
  } while (display.nextPage());
}

void drawParis()
{
  display.firstPage();
  do
  {
    display.fillScreen(GxEPD_WHITE);
    display.drawBitmap(0, 0, IMAGE_BW_P, display.epd2.WIDTH, display.epd2.HEIGHT, GxEPD_BLACK);
    display.drawBitmap(0, 0, IMAGE_RED_P, display.epd2.WIDTH, display.epd2.HEIGHT, GxEPD_RED);
  } while (display.nextPage());
  delay(5000);
}

void drawBicycle()
{
  display.firstPage();
  do
  {
    display.fillScreen(GxEPD_WHITE);
    display.drawBitmap(0, 0, IMAGE_BW, display.epd2.WIDTH, display.epd2.HEIGHT, GxEPD_BLACK);
    display.drawBitmap(0, 0, IMAGE_RED, display.epd2.WIDTH, display.epd2.HEIGHT, GxEPD_RED);
  } while (display.nextPage());
  delay(2000);
}

void fillWhite()
{
  display.firstPage();
  do
  {
    display.fillScreen(GxEPD_WHITE);
  } while (display.nextPage());
}

void setup()
{
  pinMode(33, OUTPUT);
  digitalWrite(33, HIGH); // enable power to the panel
  display.init(115200, true, 2, false);
  helloWorld();
  // delay(60000);
  // drawParis();
  // delay(60000);
  // drawBicycle();
  fillWhite();
  display.hibernate();
}

void loop() {};