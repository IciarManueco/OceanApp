package com.web.Oceano.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

// Esta clase define configuraciones globales para la aplicación
@Configuration
public class AppConfig {

    // Bean para permitir inyección de un cliente HTTP RestTemplate (para llamadas HTTP)
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    // Configuración global de CORS (Cross-Origin Resource Sharing)
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                // Permite peticiones desde el origen http://localhost:5000 (donde está Flask)
                registry.addMapping("/**")
                        .allowedOrigins("http://localhost:5000")
                        .allowedMethods("GET", "POST", "PUT", "DELETE");
            }
        };
    }
}
