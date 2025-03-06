#include "lib/util.h"

#define MIN_OUTPUT 5
#define I_MAX 100

struct PidCtrl
{
	float gainP;
	float gainI;
	float gainD;

	int integral;
	int lastInput;

	int target;
	int output;

	bool log;
}

void pid_update(PidCtrl* ctrl, int latest)
{
	int error = ctrl->target - latest;
	float termP = ctrl->gainP * error;
	ctrl->integral += error;
	//clamp the integral value
	ctrl->integral = clamp(ctrl->integral, -I_MAX, I_MAX);
	float termI = ctrl->gainI * ctrl->integral;
	float termD = ctrl->gainD * (latest - ctrl->lastInput);
	ctrl->lastInput = latest;
	ctrl->output = clamp_motor(termP + termI - termD);
	if (abs(ctrl->output) < MIN_OUTPUT)
	{
		ctrl->output = 0;
	}
	if (ctrl->log)
	{
		datalogDataGroupStart();
		datalogAddValue(0, ctrl->output);
		datalogAddValue(1, error);
		datalogAddValue(2, ctrl->target);
		datalogAddValue(3, latest);
		datalogDataGroupEnd();
	}
}