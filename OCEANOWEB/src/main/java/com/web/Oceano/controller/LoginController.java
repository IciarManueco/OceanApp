package com.web.Oceano.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

// Controlador MVC para la página de login
@Controller
public class LoginController {

    // Mapea la ruta "/login" a este método
    @GetMapping("/login")
    public String mostrarLogin() {
        // Devuelve el nombre de la vista "login", que corresponde al archivo templates/login.html
        return "login";
    }
}
