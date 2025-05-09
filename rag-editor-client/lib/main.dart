import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RAG Editor',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const RagEditorScreen(),
    );
  }
}

class RagEditorScreen extends StatefulWidget {
  const RagEditorScreen({super.key});

  @override
  _RagEditorScreenState createState() => _RagEditorScreenState();
}

class _RagEditorScreenState extends State<RagEditorScreen> {
  final TextEditingController _controller = TextEditingController();
  bool _isLoading = false;
  final String serverUrl = "http://94.241.143.115:5000/api/rag"; // Замените на реальный IP

  Future<void> _loadRag() async {
    setState(() => _isLoading = true);
    try {
      final response = await http.get(Uri.parse(serverUrl));
      if (response.statusCode == 200) {
        _controller.text = jsonDecode(response.body)['text'];
      }
    } catch (e) {
      _showError(e.toString());
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _saveRag() async {
    setState(() => _isLoading = true);
    try {
      final response = await http.post(
        Uri.parse(serverUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'text': _controller.text}),
      );
      if (response.statusCode != 200) throw Exception('Ошибка сохранения');
      _showSuccess();
    } catch (e) {
      _showError(e.toString());
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.red),
    );
  }

  void _showSuccess() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Успешно сохранено!'), backgroundColor: Colors.green),
    );
  }

  @override
  void initState() {
    super.initState();
    _loadRag();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Редактор RAG-запроса')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      maxLines: null,
                      expands: true,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'Введите ваш RAG-запрос...',
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      ElevatedButton(
                        onPressed: _loadRag,
                        child: const Text('Обновить'),
                      ),
                      ElevatedButton(
                        onPressed: _saveRag,
                        child: const Text('Сохранить'),
                      ),
                    ],
                  ),
                ],
              ),
            ),
    );
  }
}