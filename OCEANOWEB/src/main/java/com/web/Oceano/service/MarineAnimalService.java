package com.web.Oceano.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Servicio que encapsula la lógica de negocio para consumir la API de animales marinos
@Service
public class MarineAnimalService {

    // Inyección de valores desde application.properties
    @Value("${marine.api.url}")
    private String marineApiUrl;

    @Value("${marine.api.key}")
    private String apiKey;

    private final RestTemplate restTemplate;

    // Constructor con inyección de dependencias
    public MarineAnimalService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    // Obtener todos los animales con un límite
    public ResponseEntity<?> getAllAnimals(int limit) {
        // Construye la URL de la API con los parámetros necesarios
        String url = UriComponentsBuilder.fromHttpUrl(marineApiUrl + "/species")
                .queryParam("limit", limit)
                .queryParam("api_key", apiKey)
                .toUriString();

        try {
            Map<String, Object> response = restTemplate.getForObject(url, Map.class);
            List<Map<String, Object>> animales = transformApiResponse(response);
            return ResponseEntity.ok(Map.of("data", animales, "count", animales.size()));
        } catch (Exception e) {
            return buildErrorResponse(500, "Error al conectar con la API de animales marinos", e.getMessage());
        }
    }

    // Obtener un animal por su ID
    public ResponseEntity<?> getAnimalById(String id) {
        String url = UriComponentsBuilder.fromHttpUrl(marineApiUrl + "/species/" + id)
                .queryParam("api_key", apiKey)
                .toUriString();

        try {
            Map<String, Object> response = restTemplate.getForObject(url, Map.class);
            Map<String, Object> animal = transformAnimalData(response);
            return ResponseEntity.ok(Map.of("data", animal));
        } catch (Exception e) {
            return buildErrorResponse(404, "Animal marino no encontrado", e.getMessage());
        }
    }

    // Buscar animales por nombre o hábitat
    public ResponseEntity<?> searchAnimals(String query, String habitat) {
        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl(marineApiUrl + "/species/search")
                .queryParam("api_key", apiKey);

        if (query != null && !query.isEmpty()) {
            builder.queryParam("name", query);
        }
        if (habitat != null && !habitat.isEmpty()) {
            builder.queryParam("habitat", habitat);
        }

        try {
            Map<String, Object> response = restTemplate.getForObject(builder.toUriString(), Map.class);
            List<Map<String, Object>> animales = transformApiResponse(response);
            return ResponseEntity.ok(Map.of("data", animales, "count", animales.size()));
        } catch (Exception e) {
            return buildErrorResponse(500, "Error en la búsqueda", e.getMessage());
        }
    }

    // Transforma la respuesta de la API a una lista de animales con formato personalizado
    private List<Map<String, Object>> transformApiResponse(Map<String, Object> apiResponse) {
        List<Map<String, Object>> animales = new ArrayList<>();
        if (apiResponse == null || !apiResponse.containsKey("results")) {
            return animales;
        }
        List<Map<String, Object>> results = (List<Map<String, Object>>) apiResponse.get("results");
        for (Map<String, Object> animalData : results) {
            animales.add(transformAnimalData(animalData));
        }
        return animales;
    }

    // Formatea un solo animal
    private Map<String, Object> transformAnimalData(Map<String, Object> animalData) {
        Map<String, Object> animal = new HashMap<>();
        animal.put("id", animalData.getOrDefault("id", ""));
        animal.put("nombre", animalData.getOrDefault("name", "Nombre no disponible"));
        animal.put("especie", animalData.getOrDefault("scientific_name", "Especie no disponible"));
        animal.put("habitat", animalData.getOrDefault("habitat", "Hábitat no disponible"));
        animal.put("descripcion", animalData.getOrDefault("description", "Descripción no disponible"));
        animal.put("imagen_url", animalData.getOrDefault("image_url",
                "https://via.placeholder.com/300x200?text=Imagen+no+disponible"));
        animal.put("estadoConservacion", animalData.getOrDefault("conservation_status", "Desconocido"));
        return animal;
    }

    // Construye una respuesta de error personalizada
    private ResponseEntity<Map<String, Object>> buildErrorResponse(int status, String error, String message) {
        Map<String, Object> errorBody = new HashMap<>();
        errorBody.put("status", status);
        errorBody.put("error", error);
        errorBody.put("message", message);
        return ResponseEntity.status(status).body(errorBody);
    }
}
