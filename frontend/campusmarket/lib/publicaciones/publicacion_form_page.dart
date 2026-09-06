import 'package:flutter/material.dart';

import 'publicaciones_api.dart';


class PublicacionFormPage extends StatefulWidget {
  const PublicacionFormPage({super.key});

  @override
  State<PublicacionFormPage> createState() => _PublicacionFormPageState();
}


class _PublicacionFormPageState extends State<PublicacionFormPage> {
  final _formKey = GlobalKey<FormState>();
  final _tituloController = TextEditingController();
  final _descripcionController = TextEditingController();
  final _precioController = TextEditingController();
  final _api = PublicacionesApi();

  String _modalidad = 'venta';
  String _estado = 'usado';
  bool _guardando = false;

  @override
  void dispose() {
    _tituloController.dispose();
    _descripcionController.dispose();
    _precioController.dispose();
    super.dispose();
  }

  Future<void> _guardar() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() => _guardando = true);

    try {
      final creada = await _api.crearPublicacion(
        titulo: _tituloController.text.trim(),
        descripcion: _descripcionController.text.trim(),
        precio: double.parse(_precioController.text),
        modalidad: _modalidad,
        estado: _estado,
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Publicación #${creada['id']} guardada correctamente.',
          ),
        ),
      );

      _tituloController.clear();
      _descripcionController.clear();
      _precioController.clear();
    } on PublicacionTemporalmenteNoDisponible catch (error) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(error.mensaje),
        ),
      );
    } catch (_) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'No fue posible guardar la publicación.',
          ),
        ),
      );
    } finally {
      if (mounted) {
        setState(() => _guardando = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('CampusMarket · Nueva publicación'),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 600),
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text(
                    'Publicar un producto',
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Corte vertical S4: Flutter → FastAPI → SQLite.',
                  ),
                  const SizedBox(height: 24),

                  TextFormField(
                    controller: _tituloController,
                    decoration: const InputDecoration(
                      labelText: 'Título',
                      border: OutlineInputBorder(),
                    ),
                    validator: (value) {
                      if (value == null || value.trim().length < 3) {
                        return 'Ingresa un título de al menos 3 caracteres.';
                      }
                      return null;
                    },
                  ),

                  const SizedBox(height: 16),

                  TextFormField(
                    controller: _descripcionController,
                    maxLines: 3,
                    decoration: const InputDecoration(
                      labelText: 'Descripción',
                      border: OutlineInputBorder(),
                    ),
                    validator: (value) {
                      if (value == null || value.trim().length < 3) {
                        return 'Ingresa una descripción.';
                      }
                      return null;
                    },
                  ),

                  const SizedBox(height: 16),

                  TextFormField(
                    controller: _precioController,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Precio',
                      border: OutlineInputBorder(),
                    ),
                    validator: (value) {
                      final parsed = double.tryParse(value ?? '');

                      if (parsed == null || parsed <= 0) {
                        return 'Ingresa un precio mayor que cero.';
                      }

                      return null;
                    },
                  ),

                  const SizedBox(height: 16),

                  DropdownButtonFormField<String>(
                    initialValue: _modalidad,
                    decoration: const InputDecoration(
                      labelText: 'Modalidad',
                      border: OutlineInputBorder(),
                    ),
                    items: const [
                      DropdownMenuItem(
                        value: 'venta',
                        child: Text('Venta'),
                      ),
                      DropdownMenuItem(
                        value: 'alquiler',
                        child: Text('Alquiler'),
                      ),
                    ],
                    onChanged: (value) {
                      if (value != null) {
                        setState(() => _modalidad = value);
                      }
                    },
                  ),

                  const SizedBox(height: 16),

                  DropdownButtonFormField<String>(
                    initialValue: _estado,
                    decoration: const InputDecoration(
                      labelText: 'Estado',
                      border: OutlineInputBorder(),
                    ),
                    items: const [
                      DropdownMenuItem(
                        value: 'nuevo',
                        child: Text('Nuevo'),
                      ),
                      DropdownMenuItem(
                        value: 'usado',
                        child: Text('Usado'),
                      ),
                      DropdownMenuItem(
                        value: 'reacondicionado',
                        child: Text('Reacondicionado'),
                      ),
                    ],
                    onChanged: (value) {
                      if (value != null) {
                        setState(() => _estado = value);
                      }
                    },
                  ),

                  const SizedBox(height: 24),

                  FilledButton(
                    onPressed: _guardando ? null : _guardar,
                    child: Text(
                      _guardando
                          ? 'Guardando...'
                          : 'Crear publicación',
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
