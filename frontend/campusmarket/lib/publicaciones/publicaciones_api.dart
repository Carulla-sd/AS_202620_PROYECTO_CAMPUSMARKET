import 'dart:convert';

import 'package:http/http.dart' as http;


class PublicacionTemporalmenteNoDisponible implements Exception {
  const PublicacionTemporalmenteNoDisponible(this.mensaje);

  final String mensaje;

  @override
  String toString() => mensaje;
}


class PublicacionesApi {
  PublicacionesApi({this.baseUrl = 'http://localhost:8000'});

  final String baseUrl;

  Future<Map<String, dynamic>> crearPublicacion({
    required String titulo,
    required String descripcion,
    required double precio,
    required String modalidad,
    required String estado,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/publicaciones'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'titulo': titulo,
        'descripcion': descripcion,
        'precio': precio,
        'modalidad': modalidad,
        'estado': estado,
      }),
    );

    if (response.statusCode == 503) {
      final body = jsonDecode(response.body);

      final detail = body is Map<String, dynamic>
          ? body['detail']?.toString()
          : null;

      throw PublicacionTemporalmenteNoDisponible(
        detail ??
            'La persistencia está temporalmente no disponible. '
                'Intenta nuevamente.',
      );
    }

    if (response.statusCode != 201) {
      throw Exception('No fue posible crear la publicación.');
    }

    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<List<dynamic>> listarPublicaciones() async {
    final response = await http.get(
      Uri.parse('$baseUrl/publicaciones'),
    );

    if (response.statusCode != 200) {
      throw Exception(
        'No fue posible consultar las publicaciones.',
      );
    }

    return jsonDecode(response.body) as List<dynamic>;
  }
}
