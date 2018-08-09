package com.braintrust.snipe;

import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

public class ServletInitializer extends SpringBootServletInitializer
{

	// ==================================================================================
	// This method configures the servlet accordingly
	// ==================================================================================
	@Override
	protected SpringApplicationBuilder configure(SpringApplicationBuilder application)
	{
		return application.sources(SnipeHuntApplication.class);
	}

}
