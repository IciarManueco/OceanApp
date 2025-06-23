package com.web.Oceano.controller;

import com.web.Oceano.service.MarineAnimalService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

// Controlador REST para exponer los endpoints de animales marinos
@RestController
@RequestMapping("/api/marine-animals")
@CrossOrigin(origins = "http://localhost:5000") // Permite el acceso desde el frontend (Flask en este caso)
public class MarineAnimalController {

    private final MarineAnimalService marineAnimalService;

    // Constructor con inyección de dependencias
    public MarineAnimalController(MarineAnimalService marineAnimalService) {
        this.marineAnimalService = marineAnimalService;
    }

    // Endpoint GET para obtener todos los animales, permite limitar el número de resultados
    @GetMapping
    public ResponseEntity<?> getAllAnimals(@RequestParam(defaultValue = "20") int limit) {
        return marineAnimalService.getAllAnimals(limit);
    }

    // Endpoint GET para obtener un animal por su ID
    @GetMapping("/{id}")
    public ResponseEntity<?> getAnimalById(@PathVariable String id) {
        return marineAnimalService.getAnimalById(id);
    }

    // Endpoint GET para buscar animales según nombre o hábitat
    @GetMapping("/search")
    public ResponseEntity<?> searchAnimals(
            @RequestParam(required = false) String q,
            @RequestParam(required = false) String habitat) {
        return marineAnimalService.searchAnimals(q, habitat);
    }
}
