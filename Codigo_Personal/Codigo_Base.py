from tkinter import N
from joblib import PrintTime
import pvlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import daytime
import Funciones  
import seaborn as sns
from scipy import stats
from sklearn.metrics import mean_squared_error


#Definir Zona Horaria
tz = 'America/Bogota'
lat, lon = 9.789103, -73.722451 # 9.789103, -73.722451 Esta es las coordenas
altitude = 50

#Ubicación Geográfica
location = pvlib.location.Location(lat, lon, tz, altitude)

api_key = 'rMYPYAhkiXjb9WUAjQVU728EI59XhF2TeY9ml5cz'
email = 'da.parral@uniandes.edu.co'
elpaso_tmy, header = pvlib.iotools.get_psm3(lat, lon, api_key, email, 
                                            names='2020')

times = pd.date_range('2020-01-01 00:30:00', '2020-12-31', closed='left',
                      freq='H', tz=tz) 
solpos = pvlib.solarposition.get_solarposition(elpaso_tmy.index, lat, lon)
# remove nighttime
elpaso_tmy = elpaso_tmy.loc[solpos['apparent_elevation'] > 0, :]
solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]



#print(header)
#elpaso_tmy.head()

elpaso_tmy.DNI.to_csv(path_or_buf='path')





tracker = pvlib.tracking.singleaxis(apparent_zenith=solpos.apparent_zenith, 
                                    apparent_azimuth=solpos.azimuth, 
                                    axis_tilt=0,
                                    axis_azimuth=180, #Heading south
                                    max_angle=45, 
                                    backtrack=True, 
                                    gcr=0.2857142857142857)

tracker = tracker.fillna(0)
tracker.head()
airmass = location.get_airmass(times=times, 
                               solar_position=solpos, 
                               model='kastenyoung1989')

airmass.head()
etr_nrel = pvlib.irradiance.get_extra_radiation(datetime_or_doy=times, 
                                          method='NREL', 
                                          solar_constant=1361);
surface_albedo = pvlib.irradiance.SURFACE_ALBEDOS['soil']; # Check the surfaces albedo list with print(irradiance.SURFACE_ALBEDOS.items()) function
solpos.to_csv(path_or_buf='path2')
poa_ = pvlib.bifacial.pvfactors_timeseries(surface_tilt=tracker.surface_tilt, 
                                            surface_azimuth=tracker.surface_azimuth, 
                                            solar_zenith=solpos.zenith, 
                                            solar_azimuth=solpos.azimuth, 
                                            axis_azimuth=0,
                                            timestamps=elpaso_tmy.index,
                                            dni=elpaso_tmy.DNI, 
                                            dhi=elpaso_tmy.DHI,
                                            gcr=0.2857142857142857, 
                                            pvrow_height=1,
                                            pvrow_width=0.5,
                                            albedo=surface_albedo, 
                                            n_pvrows=5,
                                            index_observed_pvrow=4,
                                            rho_back_pvrow=0.05,
                                            rho_front_pvrow=0.03,
                                            horizon_band_angle=15)

                                            
