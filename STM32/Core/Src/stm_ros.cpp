#include <ros.h>
#include "navigation.h"
#include "motor.h"
#include <string>
#include <iostream>
#include <autonome/cmd.h>
#include <autonome/Pose.h>
using namespace std;

void publishCurrentPose();
void commandCallback(const autonome::cmdRequest & req,autonome::cmdResponse & res);
extern int PWM_L,PWM_R;
extern volatile float current_x,current_y,current_phi,current_phi;
extern volatile float kp,kd,ki;
extern volatile float right_radius,left_radius;

ros::NodeHandle nh;
autonome::Pose current_pose;
ros::Publisher pose("Pose", &current_pose);

ros::ServiceServer<autonome::cmdRequest, autonome::cmdResponse> CommandStm("stm_cmd", &commandCallback );

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart){
  nh.getHardware()->flush();
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){
  nh.getHardware()->reset_rbuf();
}

void setup(void)
{
  nh.initNode();
  nh.advertise(pose);
  nh.advertiseService(CommandStm);
}

void loop(void)
{
	publishCurrentPose();
}

void publishCurrentPose(){
	current_pose.x=current_x;
	current_pose.y=current_y;
	current_pose.phi=current_phi;
	pose.publish(&current_pose);
	nh.spinOnce();
	HAL_Delay(150);
}

void commandCallback(const autonome::cmdRequest & req,autonome::cmdResponse & res){
	if(!strcmp(req.cmd,"pwm")){
		 	 PWM_L=2000;
		     PWM_R=2000;

		     run_motors();
		     HAL_Delay(3000);
		     stop_motors();

		     res.result=true;

	}
	else if(!strcmp("test",req.cmd)){
			move_distance(500, 200);
			HAL_Delay(200);
			move_distance(-500, 200);
			HAL_Delay(200);
			rotate(90, 300);
			HAL_Delay(200);
			rotate(-90, 300);

			res.success=true;


	}
	else if(!strcmp("robotLocate",req.cmd)){
			Robot_Locate(req.x, req.y, req.speed);
			res.result=true;

	}
	else if(!strcmp("setSpacingEncoder",req.cmd)){
				setSpacingEncoder(req.x);
				res.result=true;

		}
	else if(!strcmp("moveDistance",req.cmd)){
			move_distance(req.x, req.speed);
			res.result=true;

		}
	else if(!strcmp("rotate",req.cmd)){
				rotate(req.phi, req.speed);
				res.result=true;

		}
	else if(!strcmp("orientate",req.cmd)){
					orientate(req.phi, req.speed);
					res.result=true;

	}

	else if(!strcmp("setCoords",req.cmd)){
							current_x=req.x;
							current_y=req.y;
							current_phi=req.phi;// hedhi bil degree!!!!!!!
							//current_phi_rad = req.phi/180*M_PI;
							res.result=true;

		}
	else if(!strcmp("setRaduis",req.cmd)){
								right_radius=req.x;
								left_radius=req.y;
								res.result=true;

		}
	else {
		res.result=false;
	}
}
