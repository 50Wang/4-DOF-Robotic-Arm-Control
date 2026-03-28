#ifndef _DUOJI_H
#define _DUOJI_H
#include "stm32f10x.h"

void Servo_Init(void);
void Servo_SetAngle(uint8_t ch, uint16_t angle);

#endif