Ogni sottocartella contiene due datasets:

DATASET_h:      dataset completo con 14 feature, che nell'ordine sono: 
                datetime,seconds,speed,ec,temp,do,voltage,m0_current,m1_current,latitude    
                longitude,altitude,heading,acceleration
                
DATASET_pro:    dataset processato con 23 feature che rappresentano: mean_ec	mean_do	mean_temp	mean_speed	mean_acceleration	mean_m0	mean_m1	mean_heading	mean_volt	mean_alt	std_ec	std_do	std_temp	std_speed	std_acceleration	std_m0	std_m1	std_heading	std_volt	std_alt	time	latitude	longitude
                

le medie sono state calcolate con la funzione movmean di Matlab con k = 10:
"Each mean is calculated over a sliding window of length k across neighboring elements of A. When k is odd, the window is centered about the element in the current position. When k is even, the window is centered about the current and previous elements. The window size is automatically truncated at the endpoints when there are not enough elements to fill the window. When the window is truncated, the average is taken over only the elements that fill the window." [Matlab Documentation]

le std sono state calcolate con la funzione movstd di Matlab con k = 10:
"Each standard deviation is calculated over a sliding window of length k across neighboring elements of A. When k is odd, the window is centered about the element in the current position. When k is even, the window is centered about the current and previous elements. The window size is automatically truncated at the endpoints when there are not enough elements to fill the window. When the window is truncated, the standard deviation is taken over only the elements that fill the window" [Matlab Documentation]

tutti i file sono salvati in forma testuale spaziati da tabulatura.
