import torch

def check_device():
	if torch.cuda.is_available():
		print("We do have GPU.")
		print(f"Total number of GPU we can access currently is {torch.cuda.device_count()}")
	else:
		print("We donot have GPU.")
		print(f"Total number of GPU we have access currently is zero.")


