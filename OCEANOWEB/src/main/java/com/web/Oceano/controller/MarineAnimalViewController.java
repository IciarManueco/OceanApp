package com.web.Oceano.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

// Controlador MVC que sirve la página de vista para animales marinos
@Controller
public class MarineAnimalViewController {

    @GetMapping("/marine-animals")
    public String showMarineAnimals(Model model) {
        // Agrega un atributo de modelo que será accesible en la plantilla
        model.addAttribute("pageTitle", "Explora los Animales Marinos");
        // Devuelve el nombre de la vista: templates/marine-animals.html
        return "marine-animals";
    }
}
