
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms as Trans
from scene.cameras import Camera

    
class ColmapDataset(Dataset):
    def __init__(self,
                 cameras_info,
                 resolution,
                 resolution_scale):
        self.cameras_info_dataset=cameras_info

        self.resolution=resolution
        self.resolution_scale=resolution_scale
        
    
    def __getitem__(self, idx):
        frame_cam_info=self.cameras_info_dataset[idx]
        
        cam_list=[]
        for time_idx,cam_info in enumerate(frame_cam_info):
            
            image = Image.open(cam_info.image_path)
            orig_w, orig_h = image.size

            if self.resolution in [1, 2, 4, 8]:
                resolution = round(orig_w/(self.resolution_scale * self.resolution)), round(orig_h/(self.resolution_scale * self.resolution))
            else:  # should be a type that converts to float
                if self.resolution == -1:
                    if orig_w > 1600:
                        global WARNED
                        if not WARNED:
                            print("[ INFO ] Encountered quite large input images (>1.6K pixels width), rescaling to 1.6K.\n "
                                "If this is not desired, please explicitly specify '--resolution/-r' as 1")
                            WARNED = True
                        global_down = orig_w / 1600
                    else:
                        global_down = 1
                else:
                    global_down = orig_w / self.resolution
            

                scale = float(global_down) * float(self.resolution_scale)
                resolution = (int(orig_w / scale), int(orig_h / scale))
            cam_list.append(Camera(resolution,
                        colmap_id=cam_info.uid,
                        R= cam_info.R,
                        T= cam_info.T,
                        FoVx= cam_info.FovX,
                        FoVy= cam_info.FovY,
                        image=image,
                        invdepthmap=None,
                        image_name=cam_info.image_name,
                        uid= cam_info.uid,
                        is_test_view=cam_info.is_test,
                        time_idx=cam_info.time_idx,
                        ))
        return cam_list
    

    

    def __len__(self):
        
        return len(self.cameras_info_dataset)
