from .classes.set_projects import get_and_set_active_project
# from .classes.get_config import get_config_data

class EnlightSDK:

	def __init__(self, host, token, project_name):
		self.host = host
		self.token = token
		self.project_name = project_name
		get_and_set_active_project(self.host, self.token, self.project_name)
	

	# def __init__(self):
	# 	data = get_config_data()
	# 	self.host = data["host"]
	# 	self.token = data["token"]
	# 	self.project_id = data["project_id"]
	# 	set_active_project(self.host, self.token, self.project_id)


	@property
	def DefaultPod(self):
		from .classes.default_pod import DefaultVmm
		return DefaultVmm(token=self.token, host=self.host)

	@property
	def VM(self):
		from .classes.vm import VM
		return VM(token=self.token, host=self.host)


	@property
	def Template(self):
		from .classes.template import Template
		return Template(token=self.token, host=self.host)

	@property
	def Compute(self):
		from .classes.compute import ComputeData
		return ComputeData(token=self.token, host=self.host)

	# @property
	# def Network(self):
	# 	from .classes.network import Network
	# 	return Network(token=self.token, host=self.host)

	# @property
	# def SDNNetwork(self):
	# 	from .classes.network import SDNNetwork
	# 	return SDNNetwork(token=self.token, host=self.host)



	@property
	def Flavor(self):
		from .classes.flavor import Flavor
		return Flavor(token=self.token, host=self.host)

	@property
	def Network(self):
		from .classes.ipam import Network
		return Network(token=self.token, host=self.host)

	@property
	def Ippool(self):
		from .classes.ipam import Ippool
		return Ippool(token=self.token, host=self.host)

	@property
	def Ip(self):
		from .classes.ipam import Ip
		return Ip(token=self.token, host=self.host)

	@property
	def Diskqos(self):
		from .classes.diskqos import DiskQOS
		return DiskQOS(token=self.token, host=self.host)

	@property
	def Queue(self):
		from .classes.queue import Queue
		return Queue(token=self.token, host=self.host)















	# def vm_get(self, vm_guid):
	# 	vm_get = VM.get(self.token,self.host,vm_guid)
	# 	return vm_get

	# def vm_list(self, vm_guid: Optional[str] = None, get_utilization: Optional[bool] = None, vmm_ip: Optional[str] = None, vmm_id: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None, search_text: Optional[str] = None, encryption_text: Optional[str] = None, compute_name: Optional[str] = None, vm_group: Optional[str] = None, vm_status: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None, export_type: Optional[str] = None, tools_installed: Optional[str] = None, filter_tag: Optional[str] = None, call_from: Optional[str] = None, hsgcombo: Optional[str] = None, status: Optional[str] = None, power_state: Optional[str] = None, compute_type: Optional[str] = None, is_hsg_vm: Optional[str] = None, data_from_date: Optional[str] = None, data_to_date: Optional[str] = None):
	# 	vm_list = VM.list(self.token, self.host, vm_guid=vm_guid, get_utilization=get_utilization, vmm_ip=vmm_ip, vmm_id=vmm_id, limit=limit, offset=offset, search_text=search_text, encryption_text=encryption_text, compute_name=compute_name, vm_group=vm_group, vm_status=vm_status, from_date=from_date, to_date=to_date, export_type=export_type, tools_installed=tools_installed, filter_tag=filter_tag, call_from=call_from, hsgcombo=hsgcombo, status=status, power_state=power_state, compute_type=compute_type, is_hsg_vm=is_hsg_vm, data_from_date=data_from_date, data_to_date=data_to_date)
	# 	return vm_list

	# def vm_create(self, data):
	# 	vm_create = VM.create(self.token, self.host, data)
	# 	return vm_create

	# def vm_update(self, vm_guid, data):
	# 	vm_update = VM.update(self.token, self.host, vm_guid, data)
	# 	return vm_update

	# def vm_delete(self, vm_guid, delete_mode, schedule):
	# 	vm_delete = VM.delete(self.token, self.host, vm_guid, delete_mode, schedule)
	# 	return vm_delete

