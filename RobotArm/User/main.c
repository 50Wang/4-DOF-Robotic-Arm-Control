/**
  ******************************************************************************
  * @file    ADC/3ADCs_DMA/main.c 
  * @author  MCD Application Team
  * @version V3.5.0
  * @date    08-April-2011
  * @brief   Main program body
  ******************************************************************************
  * @attention
  *
  * THE PRESENT FIRMWARE WHICH IS FOR GUIDANCE ONLY AIMS AT PROVIDING CUSTOMERS
  * WITH CODING INFORMATION REGARDING THEIR PRODUCTS IN ORDER FOR THEM TO SAVE
  * TIME. AS A RESULT, STMICROELECTRONICS SHALL NOT BE HELD LIABLE FOR ANY
  * DIRECT, INDIRECT OR CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING
  * FROM THE CONTENT OF SUCH FIRMWARE AND/OR THE USE MADE BY CUSTOMERS OF THE
  * CODING INFORMATION CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.
  *
  * <h2><center>&copy; COPYRIGHT 2011 STMicroelectronics</center></h2>
  ******************************************************************************
  */ 

/* Includes ------------------------------------------------------------------*/

#include "stm32f10x.h"

#include "delay.h"
#include "duoji.h"
#include "stm32f10x_usart.h"
#include "usart.h"	
#include "stdio.h"



int main(void)
{
    delay_init();

    Servo_Init();

    USART2_Init();

    while(1)
    {
			
    }
}









//int main(void)
//{   
//    //LineSensor_GPIO_Config();
//		//Motor_GPIO_Config();
//    //Motor_PWM_Config();
//	  delay_init();  
////	  Hongwai_GPIO_Config();
//    Servo_GPIO_Config();  
//	  Servo_PWM_Config();
//		//uart_init(9600);
//	  //GS_Init();
//	  //DY_Init();
//	  
//	  //Fan_GPIO_Config();
//    //Buzzer_GPIO_Config();
//	
//	  while(1)
//    {
//		    	//GPIO_ResetBits(GPIOA, GPIO_Pin_0);
//			   // delay_ms(1000);
//			    //GPIO_ResetBits(GPIOA, GPIO_Pin_0);
////				int iGS = Get_GS_Value();
////			  float Diany = Get_DY_Value();
////			  printf("Color:%d",iGS);
////			  printf("Voltage:%f",Diany);			
//			
//			  Servo_SetAngle(0);    // 0
//        delay_ms(1000);

//        Servo_SetAngle(45);   // 45
//        delay_ms(1000);

//        Servo_SetAngle(90);   // 90
//        delay_ms(1000);

//        Servo_SetAngle(135);  // 135
//        delay_ms(1000);

//        Servo_SetAngle(180);  // 180
//        delay_ms(1000);
//	
//			
////			  uint8_t hongwai = Read_Hongwai();		  
////        //uint8_t line = Read_LineSensor();
////			  switch(hongwai)
////				{
////					case 0x0b:// 1011
////						 TurnLeft(200);
////						 delay_ms(1000);
////					   break;
////					case 0x0e:// 1110
////						 TurnRight(200);
////					   delay_ms(1000);
////						 break;
////					default:
////                break;
////				}					
//			
////        switch (line)
////        {
////            case 0x09: // 1001 forward
////						case 0x0d: // 1101	
////						case 0x0b: // 1011
////                Forward(200);
////                break;
////            case 0x0c: // 1100 
////            case 0x08: // 1000 
////                TurnRight(200);
////                break;
////            case 0x03: // 0011 
////            case 0x01: // 0001 
////                TurnLeft(200);
////                break;
////            case 0x00:
////								Stop();
////								break;
////            default:
////                break;
////        }
//    }
//		return 0;
//}








