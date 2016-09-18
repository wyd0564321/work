package work1;

import java.net.*;  
import java.io.*; 

public class receiveServer {
	public static void main(String[] args) throws Exception{  
	    ServerSocket ss = new ServerSocket(3333); //����һ��Socket������������3333�˿�  
	    int i=0;  
	    //������ѭ����ͣ�ļ����˿�  
	    while(true){  
	      Socket s = ss.accept();//����Socket��������accept()������ȡ�ͻ���Socket����  
	      i++;  
	      System.out.println("��" + i +"���ͻ��˳ɹ����ӣ�");  
	      Client c = new Client(i,s); //�����ͻ��˴����̶߳���  
	      Thread t =new Thread(c); //�����ͻ��˴����߳�  
	      t.start(); //�����߳�  
	    }  
	  }  
}

//�ͻ��˴����߳���(ʵ��Runnable�ӿ�)  
class Client implements Runnable{  
int clientIndex = 0; //����ͻ���id  
Socket s = null; //����ͻ���Socket����  
  
Client(int i,Socket s){  
  clientIndex = i;  
  this.s = s;  
}  

//���ַ����ߵ�
public static String reverse(String s) {
	  char[] array = s.toCharArray();
	  String reverse = "";
	  for (int i = array.length - 1; i >= 0; i--)
	   reverse += array[i];
	  
	  return reverse;
	 }
  
public void run(){  
  //��ӡ���ͻ�������  
  try{  
    DataInputStream dis = new DataInputStream(s.getInputStream());  
    String importDate = dis.readUTF();
    System.out.println("��" + clientIndex + "���ͻ��˷�����Ϣ��" + importDate);  
    String outputDate = reverse(importDate);
    DataOutputStream dos = new DataOutputStream(s.getOutputStream()); 
    dos.writeUTF(outputDate);
    dos.flush();
    dis.close();  
    dos.close();
    s.close();  
  }  
  catch(Exception e)  
  {}  
}  
}  
