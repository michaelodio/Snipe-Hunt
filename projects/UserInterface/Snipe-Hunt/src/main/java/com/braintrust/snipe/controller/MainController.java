package com.braintrust.snipe.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MainController
{

	// ==================================================================================
	// This method returns a String value to map the root directory to the index page
	// ==================================================================================
	@GetMapping("/")
	public String index()
	{
		return "index";
	}

}