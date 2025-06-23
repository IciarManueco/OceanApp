package com.web.Oceano.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

// Controlador MVC que gestiona la página principal de la aplicación
@Controller
public class HomeController {

    // Mapea la ruta "/" (página de inicio) a este método
    @GetMapping("/")
    public String mostrarInicio() {
        // Devuelve el nombre de la vista "index", que corresponde al archivo templates/index.html
        return "index";
    }
}
