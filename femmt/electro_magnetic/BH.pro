Function{

  // --------------------------
  // First Example Material
  // analytical
  // analytical Brauer law for nonlinear isotropic material:
  // nu(b^2) = k1 + k2 * exp ( k3 * b^2 )
  // nu = 100. + 10. * exp ( 1.8 * b * b )
  // k1 = 100.; k2 = 10.; k3 = 1.8;
  // nu_1a[] = k1 + k2 * Exp[k3*SquNorm[$1]] ;
  // dnudb2_1a[] =  k2 * k3 * Exp[k3*SquNorm[$1]] ;
  // h_1a[] = nu_1a[$1]*$1 ;
  // dhdb_1a[] = TensorDiag[1,1,1] * nu_1a[$1#1] + 2*dnudb2_1a[#1] * SquDyadicProduct[#1]  ;
  // dhdb_1a_NL[] = 2*dnudb2_1a[$1#1] * SquDyadicProduct[#1]  ;

  // interpolated
  Mat1_h = {
    0.0000e+00, 5.5023e+00, 1.1018e+01, 1.6562e+01, 2.2149e+01, 2.7798e+01, 3.3528e+01,
    3.9363e+01, 4.5335e+01, 5.1479e+01, 5.7842e+01, 6.4481e+01, 7.1470e+01, 7.8906e+01,
    8.6910e+01, 9.5644e+01, 1.0532e+02, 1.1620e+02, 1.2868e+02, 1.4322e+02, 1.6050e+02,
    1.8139e+02, 2.0711e+02, 2.3932e+02, 2.8028e+02, 3.3314e+02, 4.0231e+02, 4.9395e+02,
    6.1678e+02, 7.8320e+02, 1.0110e+03, 1.3257e+03, 1.7645e+03, 2.3819e+03, 3.2578e+03,
    4.5110e+03, 6.3187e+03, 8.9478e+03, 1.2802e+04, 1.8500e+04, 2.6989e+04, 3.9739e+04,
    5.9047e+04, 8.8520e+04, 1.3388e+05, 2.0425e+05, 3.1434e+05, 4.8796e+05, 7.6403e+05
  } ;
  Mat1_b = {
    0.0000e+00, 5.0000e-02, 1.0000e-01, 1.5000e-01, 2.0000e-01, 2.5000e-01, 3.0000e-01,
    3.5000e-01, 4.0000e-01, 4.5000e-01, 5.0000e-01, 5.5000e-01, 6.0000e-01, 6.5000e-01,
    7.0000e-01, 7.5000e-01, 8.0000e-01, 8.5000e-01, 9.0000e-01, 9.5000e-01, 1.0000e+00,
    1.0500e+00, 1.1000e+00, 1.1500e+00, 1.2000e+00, 1.2500e+00, 1.3000e+00, 1.3500e+00,
    1.4000e+00, 1.4500e+00, 1.5000e+00, 1.5500e+00, 1.6000e+00, 1.6500e+00, 1.7000e+00,
    1.7500e+00, 1.8000e+00, 1.8500e+00, 1.9000e+00, 1.9500e+00, 2.0000e+00, 2.0500e+00,
    2.1000e+00, 2.1500e+00, 2.2000e+00, 2.2500e+00, 2.3000e+00, 2.3500e+00, 2.4000e+00
  } ;

  Mat1_b2 = Mat1_b()^2;
  Mat1_nu = Mat1_h()/Mat1_b();
  Mat1_nu(0) = Mat1_nu(1);

  Mat1_nu_b2  = ListAlt[Mat1_b2(), Mat1_nu()] ;
  nu_1[] = InterpolationLinear[ SquNorm[$1] ]{Mat1_nu_b2()} ;
  dnudb2_1[] = dInterpolationLinear[SquNorm[$1]]{Mat1_nu_b2()} ;
  h_1[] = nu_1[$1] * $1 ;
  dhdb_1[] = TensorDiag[1,1,1] * nu_1[$1#1] + 2*dnudb2_1[#1] * SquDyadicProduct[#1]  ;
  dhdb_1_NL[] = 2*dnudb2_1[$1#1] * SquDyadicProduct[#1] ;


  // --------------------------
  // Second Example Material
  // nu = 123. + 0.0596 * exp ( 3.504 * b * b )
  // analytical 3kW machine
  // nu_3kWa[] = 123. + 0.0596 * Exp[3.504*SquNorm[$1]] ;
  // dnudb2_3kWa[] = 0.0596*3.504 * Exp[3.504*SquNorm[$1]] ;
  // h_3kWa[] = nu_3kWa[$1]*$1 ;
  // dhdb_3kWa[] = TensorDiag[1,1,1] * nu_3kWa[$1#1] + 2*dnudb2_3kWa[#1] * SquDyadicProduct[#1]  ;
  // dhdb_3kWa_NL[] = 2*dnudb2_3kWa[$1#1] * SquDyadicProduct[#1]  ;

  // interpolated
  Mat3kW_h = {
    0.0000e+00, 6.1465e+00, 1.2293e+01, 1.8440e+01, 2.4588e+01, 3.0736e+01, 3.6886e+01,
    4.3037e+01, 4.9190e+01, 5.5346e+01, 6.1507e+01, 6.7673e+01, 7.3848e+01, 8.0036e+01,
    8.6241e+01, 9.2473e+01, 9.8745e+01, 1.0508e+02, 1.1150e+02, 1.1806e+02, 1.2485e+02,
    1.3199e+02, 1.3971e+02, 1.4836e+02, 1.5856e+02, 1.7137e+02, 1.8864e+02, 2.1363e+02,
    2.5219e+02, 3.1498e+02, 4.2161e+02, 6.0888e+02, 9.4665e+02, 1.5697e+03, 2.7417e+03,
    4.9870e+03, 9.3633e+03, 1.8037e+04, 3.5518e+04, 7.1329e+04, 1.4591e+05, 3.0380e+05,
    6.4363e+05, 1.3872e+06, 3.0413e+06, 6.7826e+06, 1.5386e+07, 3.5504e+07, 8.3338e+07
  } ;
  Mat3kW_b = {
    0.0000e+00, 5.0000e-02, 1.0000e-01, 1.5000e-01, 2.0000e-01, 2.5000e-01, 3.0000e-01,
    3.5000e-01, 4.0000e-01, 4.5000e-01, 5.0000e-01, 5.5000e-01, 6.0000e-01, 6.5000e-01,
    7.0000e-01, 7.5000e-01, 8.0000e-01, 8.5000e-01, 9.0000e-01, 9.5000e-01, 1.0000e+00,
    1.0500e+00, 1.1000e+00, 1.1500e+00, 1.2000e+00, 1.2500e+00, 1.3000e+00, 1.3500e+00,
    1.4000e+00, 1.4500e+00, 1.5000e+00, 1.5500e+00, 1.6000e+00, 1.6500e+00, 1.7000e+00,
    1.7500e+00, 1.8000e+00, 1.8500e+00, 1.9000e+00, 1.9500e+00, 2.0000e+00, 2.0500e+00,
    2.1000e+00, 2.1500e+00, 2.2000e+00, 2.2500e+00, 2.3000e+00, 2.3500e+00, 2.4000e+00
  } ;

  Mat3kW_b2 = Mat3kW_b()^2;
  Mat3kW_nu = Mat3kW_h()/Mat3kW_b();
  Mat3kW_nu(0) = Mat3kW_nu(1);

  Mat3kW_nu_b2  = ListAlt[Mat3kW_b2(), Mat3kW_nu()] ;
  nu_3kW[] = InterpolationLinear[SquNorm[$1]]{Mat3kW_nu_b2()} ;
  dnudb2_3kW[] = dInterpolationLinear[SquNorm[$1]]{Mat3kW_nu_b2()} ;
  h_3kW[] = nu_3kW[$1] * $1 ;
  dhdb_3kW[] = TensorDiag[1,1,1]*nu_3kW[$1#1] + 2*dnudb2_3kW[#1] * SquDyadicProduct[#1] ;
  dhdb_3kW_NL[] = 2*dnudb2_3kW[$1] * SquDyadicProduct[$1] ;


  // --------------------------
  // TDK N95

  // interpolated
  N95_h = {
0.000000000000000000e+00, 2.000000000000000000e+00, 4.000000000000000000e+00, 6.000000000000000000e+00, 8.000000000000000000e+00, 9.000000000000000000e+00, 1.000000000000000000e+01, 1.200000000000000000e+01, 1.300000000000000000e+01, 1.400000000000000000e+01, 1.600000000000000000e+01, 1.700000000000000000e+01, 1.800000000000000000e+01, 2.200000000000000000e+01, 2.400000000000000000e+01, 2.500000000000000000e+01, 2.700000000000000000e+01, 2.900000000000000000e+01, 3.100000000000000000e+01, 3.300000000000000000e+01, 3.600000000000000000e+01, 3.900000000000000000e+01, 4.200000000000000000e+01, 4.500000000000000000e+01, 4.900000000000000000e+01, 5.400000000000000000e+01, 6.700000000000000000e+01, 7.600000000000000000e+01, 8.800000000000000000e+01, 1.030000000000000000e+02, 1.240000000000000000e+02, 1.530000000000000000e+02, 1.920000000000000000e+02, 2.440000000000000000e+02, 3.100000000000000000e+02, 3.870000000000000000e+02, 4.730000000000000000e+02, 5.610000000000000000e+02, 6.490000000000000000e+02, 8.150000000000000000e+02, 8.900000000000000000e+02, 9.570000000000000000e+02, 1.017000000000000000e+03
  } ;
  N95_b = {
0.000000000000000000e+00, 1.530000000000000110e-02, 3.059999999999999873e-02, 4.589999999999999636e-02, 6.119999999999999746e-02, 7.649999999999999856e-02, 9.281999999999999973e-02, 1.081199999999999939e-01, 1.234200000000000158e-01, 1.387199999999999822e-01, 1.540199999999999902e-01, 1.703399999999999914e-01, 1.856399999999999995e-01, 2.162399999999999878e-01, 2.315399999999999958e-01, 2.468400000000000039e-01, 2.621399999999999841e-01, 2.774399999999999644e-01, 2.927400000000000002e-01, 3.070200000000000151e-01, 3.223199999999999954e-01, 3.365999999999999548e-01, 3.508799999999999697e-01, 3.651599999999999846e-01, 3.794399999999999995e-01, 3.937200000000000144e-01, 4.202400000000000024e-01, 4.334999999999999964e-01, 4.457400000000000251e-01, 4.579799999999999982e-01, 4.691999999999999504e-01, 4.793999999999999928e-01, 4.875599999999999934e-01, 4.957199999999999940e-01, 5.008200000000000429e-01, 5.049000000000000155e-01, 5.079599999999999671e-01, 5.100000000000000089e-01, 5.110200000000000298e-01, 5.130599999999999605e-01, 5.138759999999999994e-01, 5.144879999999999454e-01, 5.147940000000000849e-01
  } ;

  N95_b2 = N95_b()^2;
  N95_nu = N95_h()/N95_b();
  N95_nu(0) = N95_nu(1);

  N95_nu_b2  = ListAlt[N95_b2(), N95_nu()] ;
  nu_N95[] = InterpolationLinear[SquNorm[$1]]{N95_nu_b2()} ;
  dnudb2_N95[] = dInterpolationLinear[SquNorm[$1]]{N95_nu_b2()} ;
  h_N95[] = nu_N95[$1] * $1 ;
  dhdb_N95[] = TensorDiag[1,1,1]*nu_N95[$1#1] + 2*dnudb2_N95[#1] * SquDyadicProduct[#1] ;
  dhdb_N95_NL[] = 2*dnudb2_N95[$1] * SquDyadicProduct[$1] ;


  // --------------------------
  // TDK N95 100 Celsius

  // interpolated
  N95100_h = {
  0.0, 1.0, 3.0, 5.0, 6.0, 7.0, 8.0, 10.0, 11.0, 12.0, 14.0, 15.0, 17.0, 20.0, 22.0, 23.0, 24.0, 26.0, 28.0, 31.0, 33.0, 36.0, 39.0, 42.0, 45.0, 50.0, 70.0, 91.0, 126.0, 181.0, 255.0, 344.0, 439.0, 534.0, 625.0, 710.0, 789.0, 863.0, 930.0, 1044.0, 1089.0, 1126.0, 1155.0, 1174.0, 1188.0, 1197.0, 1202.0
    } ;
  N95100_b = {
  0.0, 0.01273, 0.025510000000000005, 0.03834, 0.05122, 0.06413, 0.07708, 0.09006, 0.10306, 0.11607999999999999, 0.1291, 0.14212, 0.15514, 0.18109, 0.19401000000000002, 0.20688, 0.21969, 0.23245, 0.24514999999999998, 0.25777, 0.27032, 0.28277, 0.29511, 0.30733, 0.31939, 0.33124, 0.35384, 0.36401, 0.37276, 0.37958000000000003, 0.38434, 0.38732, 0.3891, 0.39022, 0.39102, 0.39164, 0.39215, 0.39257000000000003, 0.39293, 0.39348, 0.39369, 0.39385, 0.39397, 0.39406, 0.39411, 0.39413, 0.39414
    } ;

  N95100_b2 = N95100_b()^2;
  N95100_nu = N95100_h()/N95100_b();
  N95100_nu(0) = N95100_nu(1);

  N95100_nu_b2  = ListAlt[N95100_b2(), N95100_nu()] ;
  nu_95100[] = InterpolationLinear[SquNorm[$1]]{N95100_nu_b2()} ;
  dnudb2_95100[] = dInterpolationLinear[SquNorm[$1]]{N95100_nu_b2()} ;
  h_95100[] = nu_95100[$1] * $1 ;
  dhdb_95100[] = TensorDiag[1,1,1]*nu_95100[$1#1] + 2*dnudb2_95100[#1] * SquDyadicProduct[#1] ;
  dhdb_95100_NL[] = 2*dnudb2_95100[$1] * SquDyadicProduct[$1] ;


  // --------------------------
  // TDK N95 25 Celsius

  // interpolated
  N95_h = {
0.000000000000000000e+00, 2.000000000000000000e+00, 4.000000000000000000e+00, 6.000000000000000000e+00, 8.000000000000000000e+00, 9.000000000000000000e+00, 1.000000000000000000e+01, 1.200000000000000000e+01, 1.300000000000000000e+01, 1.400000000000000000e+01, 1.600000000000000000e+01, 1.700000000000000000e+01, 1.800000000000000000e+01, 2.200000000000000000e+01, 2.400000000000000000e+01, 2.500000000000000000e+01, 2.700000000000000000e+01, 2.900000000000000000e+01, 3.100000000000000000e+01, 3.300000000000000000e+01, 3.600000000000000000e+01, 3.900000000000000000e+01, 4.200000000000000000e+01, 4.500000000000000000e+01, 4.900000000000000000e+01, 5.400000000000000000e+01, 6.700000000000000000e+01, 7.600000000000000000e+01, 8.800000000000000000e+01, 1.030000000000000000e+02, 1.240000000000000000e+02, 1.530000000000000000e+02, 1.920000000000000000e+02, 2.440000000000000000e+02, 3.100000000000000000e+02, 3.870000000000000000e+02, 4.730000000000000000e+02, 5.610000000000000000e+02, 6.490000000000000000e+02, 8.150000000000000000e+02, 8.900000000000000000e+02, 9.570000000000000000e+02, 1.017000000000000000e+03
  } ;
  N95_b = {
0.000000000000000000e+00, 1.530000000000000110e-02, 3.059999999999999873e-02, 4.589999999999999636e-02, 6.119999999999999746e-02, 7.649999999999999856e-02, 9.281999999999999973e-02, 1.081199999999999939e-01, 1.234200000000000158e-01, 1.387199999999999822e-01, 1.540199999999999902e-01, 1.703399999999999914e-01, 1.856399999999999995e-01, 2.162399999999999878e-01, 2.315399999999999958e-01, 2.468400000000000039e-01, 2.621399999999999841e-01, 2.774399999999999644e-01, 2.927400000000000002e-01, 3.070200000000000151e-01, 3.223199999999999954e-01, 3.365999999999999548e-01, 3.508799999999999697e-01, 3.651599999999999846e-01, 3.794399999999999995e-01, 3.937200000000000144e-01, 4.202400000000000024e-01, 4.334999999999999964e-01, 4.457400000000000251e-01, 4.579799999999999982e-01, 4.691999999999999504e-01, 4.793999999999999928e-01, 4.875599999999999934e-01, 4.957199999999999940e-01, 5.008200000000000429e-01, 5.049000000000000155e-01, 5.079599999999999671e-01, 5.100000000000000089e-01, 5.110200000000000298e-01, 5.130599999999999605e-01, 5.138759999999999994e-01, 5.144879999999999454e-01, 5.147940000000000849e-01
  } ;

  N95_b2 = N95_b()^2;
  N95_nu = N95_h()/N95_b();
  N95_nu(0) = N95_nu(1);

  N95_nu_b2  = ListAlt[N95_b2(), N95_nu()] ;
  nu_95[] = InterpolationLinear[SquNorm[$1]]{N95_nu_b2()} ;
  dnudb2_95[] = dInterpolationLinear[SquNorm[$1]]{N95_nu_b2()} ;
  h_95[] = nu_95[$1] * $1 ;
  dhdb_95[] = TensorDiag[1,1,1]*nu_95[$1#1] + 2*dnudb2_95[#1] * SquDyadicProduct[#1] ;
  dhdb_95_NL[] = 2*dnudb2_95[$1] * SquDyadicProduct[$1] ;




  // --------------------------
  // Testing
  DefineFunction[nu_lin, nu_nonlin, dhdb_NL] ;
  // linear case -- testing purposes
  h_lin[] = nu_lin[] * $1 ;
  dhdb_lin[] = nu_lin[] * TensorDiag[1.,1.,1.] ;
  dhdb_lin_NL[] = TensorDiag[0.,0.,0.] ;

}