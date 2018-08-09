package com.braintrust.snipe.form;

import org.springframework.web.multipart.MultipartFile;

public class UploadForm
{

	private String description; 
	private MultipartFile[] files;

	// ==================================================================================
	// This method returns the description variable
	// ==================================================================================
	public String getDescription()
	{
		return description;
	}

	// ==================================================================================
	// This method sets the description variable
	// ==================================================================================
	public void setDescription(String description)
	{
		this.description = description;
	}

	// ==================================================================================
	// This method returns the list of all files variable
	// ==================================================================================
	public MultipartFile[] getFiles()
	{
		return files;
	}

	// ==================================================================================
	// This method sets the list of all files variables
	// ==================================================================================
	public void setFiles(MultipartFile[] files)
	{
		this.files = files;
	}

}