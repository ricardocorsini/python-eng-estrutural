using System;
using System.Collections.Generic;
using System.Text;

namespace Meteriais
{
    class Concreto
    {
        //Todos os parâmetros da classe estão calculados em MPa EXCETO FCK QUE É RETORNADO EM kN/cm²
        public double fck { get; set; }
        public double fctk { get; set; }
        public double Eci { get; set; }


        public Concreto(double fck)
        {
            this.fck = fck/10; //Converte de MPa para kN/cm^2

        }

        public double fcd()
        {
            return ((fck*10) / 1.4)/10;
        }
        public double sigmacd()
        {
            return alphaC() * fcd();
        }
        public double alphaC()
        {
            if (fck*10 <= 50)
            {
                return 0.85;
            }
            else
            {
                return 0.85 * (1 - ((fck*10 - 50) / 200));
            }
        }
        public double lambda()
        {
            if (fck*10 <= 50)
            {
                return 0.8;
            }
            else
            {
                return 0.8 - (fck*10 - 50) / 400;
            }
        }
        public double fctk_inf()
        {
            return 0.3*0.7*Math.Pow(fck*10,(2.0/3.0));
        }





    }
}
