import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;


public class HalOperations {
	
	String linuxPass;
	
    public static void main(String[] args) {
    	//param1 linuxPass
    	
    	
    	
        HalOperations ho = new HalOperations(args[0]);


//		ho.readDevices();
//		ho.addDevice("00:00:00:00:00:11", "Test2", null, "https://icons.org/image", null, null);
//		ho.addDevice("00:00:00:00:00:88", "Test23445", null, "https://icons.org/image", null, null);
//		ho.addDevice("00:00:00:00:00:22", "Test3", "Prueba3", null, true, true);
		
//		ho.updateDevice("00:00:00:00:00:11", "Test4", null, "https://icons.org/image2", null, null);
		ho.deleteDevice("00:00:00:00:00:22");
    }
    
    
    
    public HalOperations(String linuxPass) {
		super();
		this.linuxPass = linuxPass;
		
	}
    
    public boolean addDevice(String mac, String name, String user, String picture,
    		Boolean track, Boolean hide) {
    	
    	if(mac == null || mac.length()!=17 || name == null || name.length()<1) {
    		System.out.println("Error en parámetros obligatorios");
    		return false;
    	}
    	String p_mac = " -M " + mac;
    	String p_name = " -n " + name;

    	String p_user = "";
    	String p_picture = "";
    	String p_track = "";
    	String p_hide = "";

    	if(user != null) {
        	p_user = " -u " + user;
    	}
    	if(picture != null) {
    		if(picture.startsWith("http")) {
            	p_picture = " -pu " + picture;
    		}else {
    			p_picture = " -pp " + picture;
    		}
    	}
    	if(track != null) {
        	p_track = " -t " + track;
    	}
    	if(hide != null) {
        	p_hide = " -o " + hide;
    	}
    	String command = "/home/jdavila/Escritorio/hal_scripts/add_device.py" + p_mac + p_name + p_user + p_picture + p_track + p_hide; 

    	return this.execCommand(command);
    }
    
    public boolean updateDevice(String mac, String name, String user, String picture,
    		Boolean track, Boolean hide) {
    	
    	if(mac == null || mac.length()!=17 || name == null || name.length()<1) {
    		System.out.println("Error en parámetros obligatorios");
    		return false;
    	}
    	String p_mac = " -M " + mac;
    	
    	String p_name = "";
    	String p_user = "";
    	String p_picture = "";
    	String p_track = "";
    	String p_hide = "";

    	if(name != null) {
        	p_name = " -u " + name;
    	}
    	if(user != null) {
        	p_user = " -u " + user;
    	}
    	if(picture != null) {
    		if(picture.startsWith("http")) {
            	p_picture = " -pu " + picture;
    		}else {
    			p_picture = " -pp " + picture;
    		}
    	}
    	if(track != null) {
        	p_track = " -t " + track;
    	}
    	if(hide != null) {
        	p_hide = " -o " + hide;
    	}
    	String command = "/home/jdavila/Escritorio/hal_scripts/update_device.py"
    				+ p_mac + p_name + p_user + p_picture + p_track + p_hide; 
    	
    	return this.execCommand(command);
    }
    
    public boolean deleteDevice(String mac) {
    	
    	if(mac == null || mac.length()!=17 ) {
    		System.out.println("Error en parámetro");
    		return false;
    	}
    	String p_mac = " -M " + mac;
    	
    	String command = "/home/jdavila/Escritorio/hal_scripts/delete_device.py" + p_mac; 
    	
    	return this.execCommand(command);
    }
    
    public boolean deleteDeviceWithUsername(String user) {

    	if( user == null || user.length()<1) {
    		System.out.println("Error en parámetro");
    		return false;
    	}
    	String p_user = " -u " + user;
    	
    	String command = "/home/jdavila/Escritorio/hal_scripts/delete_device.py" + p_user; 
    	
    	return this.execCommand(command);
    }
    
    public boolean readDevices() {

    	String command = "/home/jdavila/Escritorio/hal_scripts/read_devices.py"; 
    	
    	return this.execCommand(command);
    }



    private boolean execCommand(String command) {
    	
    	System.out.println("Comando: python " + command);
    	
    	boolean done = false;
    	   	
    	
    	ProcessBuilder processBuilder = new ProcessBuilder();

    	processBuilder.command("bash", "-c", "echo " +linuxPass+ "| sudo -S python " + command);

    	try {

    		Process process = processBuilder.start();

    		StringBuilder output = new StringBuilder();

    		BufferedReader reader = new BufferedReader(
    				new InputStreamReader(process.getInputStream()));

    		String line;
    		while ((line = reader.readLine()) != null) {
    			output.append(line + "\n");
    		}

    		int exitVal = process.waitFor();
    		if (exitVal == 0) {
    			System.out.println("Success!");
    			System.out.println(output);
    			done = true;
    		} else {
    			System.out.println(processBuilder.redirectErrorStream());
    		}

    	} catch (IOException e) {
    		e.printStackTrace();
    	} catch (InterruptedException e) {
    		e.printStackTrace();
    	}

    	return done;
    }
}