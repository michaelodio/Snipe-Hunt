package com.braintrust.snipe.restcontroller;

import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map.Entry;


import netscape.javascript.JSObject;
import org.mortbay.util.ajax.JSON;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.json.JSONObject;

import org.apache.accumulo.core.client.Connector;
import org.apache.accumulo.core.client.Instance;
import org.apache.accumulo.core.client.ZooKeeperInstance;
import org.apache.accumulo.core.client.security.tokens.PasswordToken;
import org.apache.accumulo.core.security.Authorizations;
import org.apache.accumulo.core.client.*;
import org.apache.accumulo.core.data.*;
import org.apache.accumulo.core.client.Scanner.*;

import com.braintrust.snipe.form.UploadForm;
import com.braintrust.snipe.status.Status;


@RestController
public class MainRESTController
{

	// Linux: /home/{user}/test
	// Windows: C:/Users/{user}/test
	private static String UPLOAD_DIR = System.getProperty("user.home") + "/Desktop/tomcat9/webapps/Snipe-Hunt/res";

	// ==================================================================================
	// This method handles the uploading of files
	// ==================================================================================
	@PostMapping("/upload")
	public ResponseEntity<?> uploadFileMulti(@ModelAttribute UploadForm form) throws Exception {
		System.out.println("Description:" + form.getDescription());
		String result = "";

		try {
			saveUploadedFiles(form.getFiles());
			getListFiles();
		} catch (IOException e) // Other Exceptions catch by RestGlobalExceptionHandler class.
		{
			e.printStackTrace();
			return new ResponseEntity<>("Error: " + e.getMessage(), HttpStatus.BAD_REQUEST);
		}

		return new ResponseEntity<List>(getListFiles(), HttpStatus.OK);
	}

	// ==================================================================================
	// This method returns accumulo table updates
	// ==================================================================================
	@GetMapping("/getAccumulo")
	public ResponseEntity<?> accumuloConnector() throws Exception 
	{
		String result = "win";
		String op = "lose";

		Value value = new Value();
		String instanceName = "bt-interns";
		String zooServers = "localhost:2181";
		Instance inst = new ZooKeeperInstance(instanceName, zooServers);
        Connector conn;
		conn = inst.getConnector("root", new PasswordToken("RoadRally4321"));

		Authorizations auths = new Authorizations();
		Scanner scan = conn.createScanner("man_waving_flag_mp4_analysis", auths);

		// loop through every table entry and set that to value
		for(Entry<Key,Value> entry : scan)
			value = entry.getValue();
		
        scan.close();
		return new ResponseEntity<String>(value.toString(), HttpStatus.OK);
	}

	// ==================================================================================
	// This method returns accumulo updates for the video tables
	// ==================================================================================
	@GetMapping("/getVideosTable")
	public ResponseEntity<?> accumuloVideoTable() throws Exception {

		Value value = new Value();
		String instanceName = "bt-interns";
		String zooServers = "localhost:2181";
		Instance inst = new ZooKeeperInstance(instanceName, zooServers);
		Connector conn;
		conn = inst.getConnector("root", new PasswordToken("RoadRally4321"));

		Authorizations auths = new Authorizations();
		Scanner scan = conn.createScanner("man_waving_flag_mp4", auths);

		List<String> jsonList = new ArrayList();
		for(Entry<Key,Value> entry : scan) {
			if (entry.getKey().getColumnFamily().toString().equals("cf1")) {
				value = entry.getValue();
				jsonList.add(value.toString());
			}
		}
		scan.close();

		return new ResponseEntity<String>(jsonList.toString(), HttpStatus.OK);

	}

	/*

	@GetMapping("/getImagesTable")
	public ResponseEntity<?> accumuloImageTable() throws Exception {

		Value value = new Value();
		String instanceName = "bt-interns";
		String zooServers = "localhost:2181";
		Instance inst = new ZooKeeperInstance(instanceName, zooServers);
		Connector conn;
		conn = inst.getConnector("root", new PasswordToken("RoadRally4321"));

		Authorizations auths = new Authorizations();
		Scanner scan = conn.createScanner("vid_mp4", auths);

		List<String> jsonList = new ArrayList();
		for(Entry<Key,Value> entry : scan) {
			if (jsonList.size() < 5) {
				if (entry.getKey().getColumnFamily().toString().equals("cf2")) {
					value = entry.getValue();
					jsonList.add(value.toString());
				}
			}
		}
		scan.close();

		return new ResponseEntity<Object>(jsonList, HttpStatus.OK);

	}
	*/






	// ==================================================================================
	// This method saves the uploaded files locally
	// ==================================================================================
	private String saveUploadedFiles(MultipartFile[] files) throws IOException
	{
		// Make sure directory exists!
		File uploadDir = new File(UPLOAD_DIR);
		uploadDir.mkdirs();

		StringBuilder sb = new StringBuilder();
		
		for (MultipartFile file : files)
		{
			if (file.isEmpty())
				continue;

			String uploadFilePath = UPLOAD_DIR + "/" + file.getOriginalFilename();
			uploadFilePath = uploadFilePath.replace("\\","/");

			// split file into bytes so it can be saved
			byte[] bytes = file.getBytes();
			Path path = Paths.get(uploadFilePath);
			Files.write(path, bytes);

			sb.append(uploadFilePath).append(", ");
		}

		return sb.toString();
	}

	// ==================================================================================
	// This method returns a list of the uploaded files
	// ==================================================================================
	@GetMapping("/getAllFiles")
	public List<String> getListFiles(){
		File uploadDir = new File(UPLOAD_DIR);
		File[] files = uploadDir.listFiles();

		List<String> list = new ArrayList<String>();
		for (File file : files)
			list.add(file.getName());

		return list;
	}

	// ==================================================================================
	// This method returns the results from a single uploaded file
	// ==================================================================================
	// @filename: abc.zip,..
	@GetMapping("/files/{filename:.+}")
	public ResponseEntity<Resource> getFile(@PathVariable String filename) throws MalformedURLException
	{
		File file = new File(UPLOAD_DIR + "/" + filename);
		if (!file.exists())
			throw new RuntimeException("File not found");

		Resource resource = new UrlResource(file.toURI());
		return ResponseEntity.ok()
				.header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + file.getName() + "\"")
				.body(resource);
	}

}