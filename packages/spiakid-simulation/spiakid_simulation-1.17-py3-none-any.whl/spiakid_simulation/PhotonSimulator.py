import numpy as np
from pathlib import Path
from scipy import signal as sg
from scipy import interpolate
import pickle
from astropy.io import fits
from scipy import interpolate
import spiakid_simulation.functions.output.HDF5_creation as hdf
import spiakid_simulation.functions.yaml.yaml_rw as yml
import spiakid_simulation.functions.noise.noise as N
import spiakid_simulation.functions.timeline.timeline as Tl
import spiakid_simulation.functions.phase.phase_conversion as Ph
import spiakid_simulation.functions.phase.calib_read as Cr
import spiakid_simulation.functions.IQ.IQ_sim as IQ
import spiakid_simulation.functions.photon.sim_image_photon as SI
import spiakid_simulation.functions.photon.rot as Rot

import spiakid_simulation.electronics.filter as Fi
import spiakid_simulation.electronics.data_reading as Re

import spiakid_simulation.image_process.image_generation as IG
import spiakid_simulation.image_process.atmosphere.turbulence as Tf

class PhotonSimulator():
    r"""" Launch the simulation by reading the yaml file and return all the computed information

    Parameter:
    ----------

    Yaml_path: string
        Path to the YAML input file

    Attributes:
    -----------

    TBD

    
    """

    def __init__(self, yaml_path):


        # Reading all config in the yaml
        self.config = yml.read_yaml(yaml_path)
        path = self.type_variable(self.config['sim_file'],'sim_file',[str])

        if Path(path).exists():
                print('Simulation exist')   # The name given to the simulation is already taken
                self.result = Re.load_dict_from_hdf5(path)

        else:
            print('Creating the simulation')
                
            sim_config = self.config['1-Photon_Generation']

            telescope = sim_config['telescope']
            pix_size = self.type_variable(telescope['detector']['pix_size'], 'pix_size',[float,int])
            exposure_time = self.type_variable(telescope['exposition_time'],'exposition_time',[float,int])
            pix_nbr = self.type_variable(telescope['detector']['pix_nbr'],'pix_nbr',[int])
            detector_dim = [pix_nbr,pix_nbr]
            tel_diam = self.type_variable(telescope['diameter'],'diameter',[float,int])
            latitude = self.type_variable(telescope['latitude'],'latitude',[float,int]) * np.pi/180
            obscuration = self.type_variable(telescope['obscuration'],'obscuration',[float,int])

            star = sim_config['star']
            nb_object = self.type_variable(star['number'],'number',[int])
            distance =  (self.type_variable(star['distance']['min'],'distance_min',[float,int]) ,self.type_variable(star['distance']['max'],'distance_max',[float,int]))
            spectrum = self.type_variable(star['spectrum_folder'],'spectrum_folder',[str])
            wavelength_array = np.linspace(self.type_variable(star['wavelength_array']['min'],'wv_min',[float,int]), self.type_variable(star['wavelength_array']['max'],'wv_max',[float,int]), self.type_variable(star['wavelength_array']['nbr'],'wv_nbr',[int]))
            
            sky = sim_config['sky']
            sky_method = self.type_variable(sky['method'],'sky_method',[str])
            alt = self.type_variable(sky['guide']['alt'],'altitude',[float,int]) * np.pi / 180 
            az = self.type_variable(sky['guide']['az'],'azimuth',[float,int]) * np.pi / 180
            contamination = self.type_variable(sky['contamination'],'contamination',[bool])
            rotation = self.type_variable(sky['rotation'],'rotation',[bool])

            if self.type_variable(sky['fov_method'],'fov_method',[str]) == 'fix':
                sky_fov = pix_size
            elif self.type_variable(sky['fov_method'],'fov_method',[str]) == 'time_dep':
                sky_fov = int(pix_size + exposure_time/100)   # A revoir !
            else:
                print('sky FOV is not defined')

                
            #   Creation of stars with their spectrum
            self.star_pos,self.star_spec = IG.image_sim(Image_size=int(pix_nbr/pix_size*sky_fov), object_number=nb_object, distance=distance, Path_file=path,Wavelength=wavelength_array,spectrum = spectrum,save = False)

            rot = np.zeros(len(self.star_pos),dtype = object)
            alt_ev = np.zeros(len(self.star_pos),dtype = object)

            #   Rotation effect
            if rotation == True:
                print('Earth rotation effect')
                coo_guide = [alt,az]
                for st in range(len(self.star_pos)):
                    rot[st],alt_ev[st] =Rot.rotation(lat_tel=latitude,coo_guide=coo_guide,coo_star=self.star_pos[st], time = exposure_time,size=pix_nbr)

            else:
                for st in range(len(self.star_pos)):
                    rot[st] = [interpolate.interp1d([0,exposure_time],[self.star_pos[st][1],self.star_pos[st][1]]),interpolate.interp1d([0,exposure_time],[self.star_pos[st][2],self.star_pos[st][2]])]
                    alt_ev[st] = interpolate.interp1d([0,exposure_time],[np.pi/2,np.pi/2])
                

                    
            try: trans_Path = self.type_variable(telescope['transmittance'],'transmittance',[str])
            except: trans_Path = False

            #   Creation of photons
            self.photon_list = SI.photon(wavelength_array,self.star_spec,exposure_time,tel_diam,trans_Path)   
                
                #   Point Source Function
            try: sim_config['PSF']
            except:
                print('No PSF -> Point')
                psf_grid = np.zeros(shape = (pix_nbr,pix_nbr,len(wavelength_array)))
                psf_grid[int(pix_nbr/2),int(pix_nbr/2),:] = 1
                point = np.linspace(0,1,pix_nbr)
                psf = interpolate.RegularGridInterpolator((point,point,wavelength_array),psf_grid)
                self.psf_visu = psf_grid
            else:
                if self.type_variable(sim_config['PSF']['method'],'method',[str]) == 'turbulence':
                    print('PSF computing')
                    turb = sim_config['PSF']  
                    seeing = self.type_variable(turb['seeing'],'seeing',[float,int])
                    wind = self.type_variable(turb['wind'],'wind',[float,int,tuple,list])
                    L0 = self.type_variable(turb['L0'],'L0',[float,int])
                    psf_pix_nbr = self.type_variable(turb['pix_nbr'],'pix_nbr',[int])
                    try: save_link = turb['file'] 
                    except: save_link = 0
                    if np.shape(wind)==():
                        self.psf_visu = Tf.PSF_creation(pix_size * pix_nbr, psf_pix_nbr, wavelength_array, seeing, wind, tel_diam, obscuration, L0,exposure_time,save_link)
                    else:
                        coeff = self.type_variable(turb['coeff'],'coeff',[list,tuple])
                        self.psf_visu = Tf.PSF_creation_mult(pix_size*pix_nbr, psf_pix_nbr,  wavelength_array, seeing, wind, tel_diam, obscuration, L0,exposure_time,coeff,save_link)
                elif self.type_variable(sim_config['PSF']['method'],'method',[str]) == 'Download': 
                        file = fits.open(self.type_variable(turb['file'],'PSF_file',[str]))[0]
                        self.psf_visu = file.data
                        file.close()

                points = np.linspace(0,1,psf_pix_nbr)
                psf = interpolate.RegularGridInterpolator((points,points,wavelength_array),self.psf_visu)
            print('Computing position')
            # Computing position of photon on the PSF 
            max_psf = []
            max_point = np.linspace(0,len(wavelength_array)-1,len(wavelength_array))
            for i in range(len(max_point)): max_psf.append(np.max(self.psf_visu[:,:,i])+0.01)
            # we add 0.01 to be sure to be above
            interp_point = np.linspace(wavelength_array[0],wavelength_array[-1],len(wavelength_array))
            max_func = interpolate.interp1d(interp_point, max_psf)
            
            self.photon_dict_on_PSF = SI.photon_pos_on_PSF(self.star_pos, self.photon_list, psf, np.shape(self.psf_visu)[0],max_func)
            lam0 = (max(wavelength_array)+min(wavelength_array))/2
            psf2detect = np.shape(self.psf_visu)[0] / pix_nbr
            self.photon_dict = SI.photon_proj(self.photon_dict_on_PSF,self.star_pos,psf2detect,rot,alt_ev,pix_nbr,pix_size,lam0)
            self.wavelength, self.time = SI.detector_scale(detector_dim=detector_dim, photon_dict=self.photon_dict)
            

        

            # Do we want to simulate the phase or IQ ?
            try:self.config['3-Phase']
            except:
                # We don't want to simulate the phase
                try: self.config['3-IQ']
                # We don't want to simulate nor the phase neither IQ
                except: pass
                # We want to simulate IQ
                else:
                    #   NOT UPDATED
                    # Creation of the Timeline
                    point_nb = self.type_variable(self.config['2-Timeline']['point_nb'],'point_nb',[int])
                    print('Timeline creation')
                    self.photon_timeline = Tl.sorting(exposure_time,self.wavelength,point_nb,self.time) 
                    self.IQ_Compute(obj = '3-IQ')

            else:

                # Creation of the Timeline
                point_nb = self.type_variable(self.config['2-Timeline']['point_nb'],'point_nb',[int])
                print('Timeline creation')
                self.photon_timeline = Tl.sorting(exposure_time,self.wavelength,point_nb,self.time) 
                self.phase_compute(detector_dim=detector_dim,obj = '3-Phase',timeline=self.photon_timeline, Filter = False)

            try:self.config['4-Electronic']
            except:
                pass
            else:
                wavelength, photon_time = np.zeros(detector_dim,dtype = float), np.zeros(detector_dim, dtype = float)
                photon_timeline = Tl.sorting(exposure_time,wavelength,point_nb,photon_time)
                self.phase_compute(detector_dim=detector_dim,obj = '3-Phase',timeline=photon_timeline, Filter = True)

            try: self.config['5-Output']['save']
            except: pass
            else:
                if self.type_variable(self.config['5-Output']['save'],'save',[str]) == 'Simulation':
                    print('Saving in HDF5 at: ' + str(path))
                    hdf.save_dict_to_hdf5(self.config, path,self,pix_nbr)

                elif self.type_variable(self.config['5-Output']['save'],'save',[str]) == 'photon_list':
                    print('Saving the photon list at:' +str(path))
                    hdf.save_photon_list(path,self.config, self.fil_phase,self.filtered_noise)




    def phase_compute(self, detector_dim, obj, timeline, Filter = False):

            # Reading convertion coeff
            try: self.config[obj]['Conv_wv'] and self.config[obj]['Conv_phase']
            except: 
                try: self.config[obj]['Calib_File']
                except: 
                    Cr.write_csv('Calib.csv',dim = detector_dim, sep = '/')
                    pix,conv_wv,conv_phase = Cr.read_csv('Calib.csv')
                else: pix,conv_wv,conv_phase = Cr.read_csv(self.type_variable(self.config[obj]['Calib_File'],'Calib_file',[str]))

            else:
                pix = []
                conv_wv = []
                conv_phase = []
                for i in range(detector_dim[0]):
                    for j in range(detector_dim[1]):
                        pix.append(str(i)+'_'+str(j))
                        conv_wv.append(self.config[obj]['Conv_wv'])
                        conv_phase.append(self.config[obj]['Conv_phase'])
            phase_noise = self.type_variable(self.config[obj]['Phase_Noise'],'Phase_noise',[float,int])
            decay = - self.type_variable(self.config[obj]['Decay'],'Decay',[float,int])
            
            #Conversion photon to phase
            if Filter == False:
                print('Computing phase')
                self.phase_conversion = Ph.phase_conv(timeline,pix = pix,conv_wv=conv_wv, conv_phase=conv_phase, resolution = phase_noise)
                
                #Adding exponential
                self.phase_exp = Ph.exp_adding(self.phase_conversion, decay)

                # Adding Noise
                if self.config[obj]['Readout_Noise']['type'] == 'Gaussian':
                    phase = np.copy(self.phase_exp)
                    
                    scale = self.type_variable(self.config[obj]['Readout_Noise']['scale'],'scale',[float,int])
                    self.phase =  N.gaussian(phase,scale=scale)
                elif self.config[obj]['Readout_Noise']['type'] == 'Poisson':
                    phase = np.copy(self.phase_exp)
                    self.phase = N.poisson(phase)
                else:
                    pass
            
            elif Filter == True:
                print('Filtering the phase')
                try: self.config['4-Electronic']['file']
                except: 
                    self.noise = Ph.phase_conv(timeline,pix = pix,conv_wv=conv_wv, conv_phase=conv_phase, resolution = phase_noise)
                    # Adding Noise
                    if self.config[obj]['Readout_Noise']['type'] == 'Gaussian':
                        phase = np.copy(self.noise)
                        scale = self.type_variable(self.config[obj]['Readout_Noise']['scale'],'scale',[float,int])
                        self.noise =  N.gaussian(phase,scale=scale)
                    elif self.config[obj]['Readout_Noise']['type'] == 'Poisson':
                        phase = np.copy(self.noise)
                        self.noise = N.poisson(phase)
                    else:
                        pass
                    # Filter creation

                    nperseg = self.type_variable(self.config['4-Electronic']['nperseg'],'nperseg',[int])
                    template_time = self.type_variable(self.config['4-Electronic']['template_time'],'template_time',[float,int])
                    trigerinx = self.type_variable(self.config['4-Electronic']['trigerinx'],'trigerinx',[int])
                    point_nb = self.type_variable(self.config['4-Electronic']['point_nb'],'point_nb',[int])
                    self.psd = Fi.psd(self.noise,nperseg)
                    self.template = Fi.template(self.noise, decay=decay, template_time=template_time, trigerinx=trigerinx,point_nb=point_nb)
                    self.filter = Fi.filter_creation(Noise = self.noise, template=self.template, psd=self.psd)
                    self.filtered_noise = Fi.filtering(self.noise,self.filter)
                    try: self.config['4-Electronic']['save_file']
                    except: pass
                    else:
                        file = open(self.config['4-Electronic']['save_file'], 'wb')
                        pickle.dump([self.filter,self.noise], file)
                        file.close
                else: 
                    file = open(self.config['4-Electronic']['file'],'rb')
                    self.filter,self.filtered_noise= pickle.load(file)
                    file.close()
 
                self.fil_phase = Fi.filtering(self.phase,self.filter)


     
    
    def IQ_Compute(self,obj):

            try: self.config[obj]['Calib_file_csv']
            except:
                self.IQ_conversion = IQ.photon2IQ_th(self.Photon_Timeline)
            else:
                self.IQ_conversion = IQ.photon2IQ_csv(self.Photon_Timeline, Path = self.config[obj]['Calib_file_csv'])
            Decay = self.config[obj]['Decay']
            self.IQ_exp = IQ.exp_adding(self.IQ_conversion, Decay)
            # Adding Noise
            if self.config[obj]['Readout_Noise']['type'] == 'Gaussian':
                    sig = np.copy(self.IQ_exp)
                    scale = self.config[obj]['Readout_Noise']['scale']
                    self.IQ =  [N.gaussian(sig[0],scale=scale),N.gaussian(sig[1],scale=scale)]
            elif self.config[obj]['Readout_Noise']['type'] == 'Poisson':
                    sig = np.copy(self.IQ_exp)
                    self.IQ = [N.poisson(sig[0]),N.poisson(sig[1])]
            else:
                    pass
            
    def type_variable(self,var,var_name,tp):
      
        if type(var) in tp:
            return(var)
        else: 
            raise Exception (var_name+" should be "+str(tp[0]))




