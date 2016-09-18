package work1;

import java.net.*;  
import java.io.*; 

public class receiveServer {
	public static void main(String[] args) throws Exception{  
	    ServerSocket ss = new ServerSocket(3333); //创建一个Socket服务器，监听3333端口  
	    int i=0;  
	    //利用死循环不停的监听端口  
	    while(true){  
	      Socket s = ss.accept();//利用Socket服务器的accept()方法获取客户端Socket对象。  
	      i++;  
	      System.out.println("第" + i +"个客户端成功连接！");  
	      Client c = new Client(i,s); //创建客户端处理线程对象  
	      Thread t =new Thread(c); //创建客户端处理线程  
	      t.start(); //启动线程  
	    }  
	  }  
}

//客户端处理线程类(实现Runnable接口)  
class Client implements Runnable{  
int clientIndex = 0; //保存客户端id  
Socket s = null; //保存客户端Socket对象  
  
Client(int i,Socket s){  
  clientIndex = i;  
  this.s = s;  
}  

//将字符串颠倒
public static String reverse(String s) {
	  char[] array = s.toCharArray();
	  String reverse = "";
	  for (int i = array.length - 1; i >= 0; i--)
	   reverse += array[i];
	  
	  return reverse;
	 }
  
public void run(){  
  //打印出客户端数据  
  try{  
    DataInputStream dis = new DataInputStream(s.getInputStream());  
    String importDate = dis.readUTF();
    System.out.println("第" + clientIndex + "个客户端发出消息：" + importDate);  
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
