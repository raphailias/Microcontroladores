 #include "mbed.h"
 #include "Dht11.h"

 Serial pc(PA_9, PA_10,9600);
 Dht11 sensor(PA_1);
 AnalogIn Humidadesolopin(PA_5);
 DigitalOut  myled(PA_7);
 AnalogIn LDR(PA_6);
 
 void stateMedicao(void);
 void stateControlefan(void);
 void stateControlebomba(void);
 void stateUpdate(void);
 void Inicial(void);
 // cria os estados 
 typedef enum {STATE_Medicao=0,STATE_Controlefan,STATE_Controlebomba,STATE_Update} State_Type;
 // cria uma tabela de pointers
 static void (*state_table[]) (void)={stateMedicao,stateControlefan,stateControlebomba,stateUpdate};
 // declaração global
 static State_Type curr_state;
 static int output;
 static float temperatura;
 static float humidadeAr;
 static float humidadeSolo;
 static double ldr;
 static bool ventiladorligado = true;
 static float TESTE;
 static bool bombaLigada;
 int i;
 Timer t;

void stateMedicao(){
     sensor.read();
     temperatura = sensor.getCelsius();
     humidadeAr = sensor.getHumidity();
     humidadeSolo = (Humidadesolopin.read()/1023)*3.3;
     ldr = LDR.read_u16();
     pc.printf("Temperatura :%f\n,Humidade: %f\n,Humidade do Solo: %f\n,LDR: %f\n,Ventilador :%s\n,Bomba :%s\n",temperatura,humidadeAr,humidadeSolo,ldr,ventiladorligado ? "true" : "false",bombaLigada ? "true" : "false");
     curr_state = STATE_Controlefan;

 }
 void stateControlefan(){
     if(humidadeAr <= 40){
         // DESLIGA O FAN
         ventiladorligado = false;
         myled = ventiladorligado;
     }else{ 
     if(temperatura>= 25 || humidadeAr>=50 ){
         //LIGA O FAN 
         ventiladorligado = true;
         myled = ventiladorligado;
     }
     }
     curr_state = STATE_Controlebomba;
 }
 void stateControlebomba(){
     if(humidadeSolo <= 30){
        bombaLigada = true; 
         t.start();
         while(t.read_ms() <= 5000){
         }
         t.stop();
         bombaLigada = false; 
         
     }
     curr_state = STATE_Update;

 }
 void stateUpdate(){
     sensor.read();
     temperatura = sensor.getCelsius();
     humidadeAr = sensor.getHumidity();
     humidadeSolo = Humidadesolopin.read();
     humidadeSolo = (0.030*humidadeSolo)/100;
     ldr = LDR.read_u16();
     pc.printf("Temperatura :%f\n,Humidade: %f\n,Humidade do Solo: %f\n,LDR: %f\n,Ventilador :%s\n,Bomba :%s\n",temperatura,humidadeAr,humidadeSolo,ldr,ventiladorligado ? "true" : "false",bombaLigada ? "true" : "false");
     // MANDA POR BLUETOOTH
     //RX TX COM O NODE PARA WIFI
     curr_state = STATE_Medicao;
     

     
    

    

 }
 void Inicial(){
     curr_state = STATE_Medicao;
     pc.printf("iniciou dnv");

 }

 int main() {
     Inicial();
     pc.printf("Inicio");

    while(1){
        wait(5);
        state_table[curr_state]();
    }
 }
 
