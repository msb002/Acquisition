def HVOF_Calc(arr):
    #Heat capacity of Water (J/KgC)
    C_w = 4185.5

    #Density of water (Kg/L)
    rho_w = 1

    #Standard Temperature of Alicats (K)
    Ts = 298.15

    #Standard Pressure of Alicats (PSI)
    Ps = 14.696

    #Density of Oxygen from Ideal Gas Law (g/L)
    rho_O = 32/22.4

    #Density of Kerosene (g/L)
    rho_kero = 0.8148

    #Heat/mass of kerosene (J/kg)
    Q_kero = 64.0E6

    #Stoichiometric Ratio 
    stoich = 170.0/592.0

    
    Fl_fuel, Fl_w, T_in, T_out, m_dot_O = arr #in [lpm, lpm, C, C, SLPM]
    
    #Phi Calculation: mass flow is calculated in g/min
    m_dot_fuel = Fl_fuel * rho_kero * 1000 #1000g/1kg
    phi = (m_dot_fuel/m_dot_O)/stoich
    
    #Heat Calculations
    Q_w = (T_out-T_in)*C_w*Fl_w*rho_w * (1/60.0) #1min/60seconds
    
    Q_fuel = Fl_fuel*rho_kero* Q_kero * (1/60.0) #1min/60seconds
    
    return [phi, Q_w, Q_fuel]
    
    
