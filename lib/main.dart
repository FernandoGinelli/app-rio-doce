
import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:syncfusion_flutter_charts/charts.dart';


List<String> expressedIn = [];
List<String> measured = [];
List<String> participatedIn = [];



class PieChartWithLegend extends StatelessWidget {
  final List<Measurement> measurements;

  PieChartWithLegend({required this.measurements});

  @override
  Widget build(BuildContext context) {
    var black;
    int i=0;
    return Container(
      width: 500, // Defina o tamanho desejado para o gráfico
      height: 500,

      child: SfCartesianChart(
        // Initialize category axis
        primaryXAxis: CategoryAxis(),

        series: <ChartSeries>[
          BarSeries<Measurement, String>(
            dataSource: measurements,
            xValueMapper: (Measurement data, _) => data.measured,
            yValueMapper: (Measurement data, _) => data.hasQualityValue,


          ),
        ],
      ),
    );

  }
}


class Measurement {
  final String measured;
  final String expressedIn;
  late final double hasQualityValue;
  final String hasBeginPointInXSDDateTimeStamp;

  Measurement({
    required this.measured,
    required this.expressedIn,
    required this.hasQualityValue,
    required this.hasBeginPointInXSDDateTimeStamp,
  });

  factory Measurement.fromJson(Map<String, dynamic> json) {
    return Measurement(
      measured: json['measured'],
      expressedIn: json['expressedIn'],
      hasQualityValue: double.parse(json['hasQualityValue']),
      hasBeginPointInXSDDateTimeStamp: json['hasBeginPointInXSDDateTimeStamp'],
    );
  }
}
void main() {

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MAPA COM PONTOS DE COLETA DE QUALIDADE DA AGUA DO RIO DOCE',
      home: MapScreen(),
    );
  }
}

class MapScreen extends StatefulWidget {
  @override
  _MapScreenState createState() => _MapScreenState();
}

String agent = '';
 String expressedInApi = '';
 String measuredApi = '';

class _MapScreenState extends State<MapScreen> {

  final LatLng _markerLocation = const LatLng(-19.51064, -40.554916); // coordenadas da marcação

  List<LatLng> _locations = [];
  late String filter1Value = '';



  @override
  void initState() {
    super.initState();
    _fetchLocations();
    _fetchData();
  }


  Future<void> _fetchData() async {
    final url = 'http://localhost:5000/combo';


    try {
    final response = await http.get(Uri.parse(url));

    if (response.statusCode == 200) {
    // Decodifique a resposta JSON
    final decodedData = json.decode(response.body);

    // Preencha os arrays
    expressedIn = List<String>.from(decodedData['expressedIn']);
    measured = List<String>.from(decodedData['measured']);
    participatedIn = List<String>.from(decodedData['participatedIn']);


    }
    else {
    print('Erro na requisição: ${response.statusCode}');
      }
    } catch (e) {
    print('Erro ao carregar os dados: $e');
    }
}

  void _fetchLocations() async {
    final response = await http.get(Uri.parse('http://localhost:5000/points'));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as List<dynamic>;
      setState(() {
        _locations = data
            .map((item) => LatLng(
          double.parse(item['lat']),
          double.parse(item['long']),
        ))
            .toList();
      });
    }
  }




  MapController _mapController = MapController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AGUA DO RIO DOCE'),
      ),
      drawer: Drawer(
        child: ListView(

          padding: EdgeInsets.zero,
          children: [
            const DrawerHeader(

              child: Text(
                  'Filtros',
                  style: TextStyle(

                  fontSize: 50.0,  // Ajuste o tamanho do texto aqui
                  color: Colors.white,
              )),
              decoration: BoxDecoration(

                color: Colors.blue,
              ),
            ),
             DropdownMenuExample(),
              SizedBox(height: 10),

            DropdownUnidadedeMedida(),
            SizedBox(height: 10),

            DropdownQualidadeMedida(),

          ],
        ),
      ),
      body: Stack(
        children: [
          FlutterMap(
            options: MapOptions(
              center: _markerLocation,
              zoom: 10,
              maxZoom: 18.49,
              onPositionChanged: (position, hasGesture) {
                // Você pode acessar a posição e verificar se houve um gesto de zoom ou pan
                // para atualizar a interface de acordo, se necessário.
              },
            ),
            mapController: _mapController,
            children: [
              TileLayer(
                urlTemplate: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                subdomains: ['a', 'b', 'c'],
              ),
              MarkerLayer(
                markers: _locations
                    .map(
                      (location) => Marker(
                    width: 40.0,
                    height: 40.0,
                    point: location,
                    builder: (ctx) => GestureDetector(
                      onTap: () {
                        _showCoordinate(location);
                      },
                      child: Container(
                        child: const Icon(Icons.location_pin),
                      ),
                    ),
                  ),
                )
                    .toList(),
              ),
            ],
          ),
          Positioned(
            bottom: 16,
            right: 16,
            child: FloatingActionButton(
              onPressed: () {
                _resetZoom();
              },
              child: const Icon(Icons.zoom_out),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _showCoordinate(LatLng location) async {
    final completer = Completer<void>();

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return FutureBuilder<void>(
          future: completer.future,
          builder: (BuildContext context, AsyncSnapshot<void> snapshot) {
            if (snapshot.connectionState == ConnectionState.done) {
              return AlertDialog(
                title: const Text('Coordenada'),
                content: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Latitude: ${location.latitude}\nLongitude: ${location.longitude}'),
                    const SizedBox(height: 16),
                    Text('Aguarde, carregando dados...'),
                  ],
                ),
                actions: [
                  TextButton(
                    child: const Text('Fechar'),
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                  ),
                ],
              );
            } else {
              return AlertDialog(
                title: const Text('Coordenada'),
                content: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Latitude: ${location.latitude}\nLongitude: ${location.longitude}'),
                    const SizedBox(height: 16),
                    CircularProgressIndicator(),
                  ],
                ),
              );
            }
          },
        );
      },
    );
    agent= agent.isEmpty ? 'null': agent;
    expressedInApi= expressedInApi.isEmpty ? 'null': expressedInApi;
    measuredApi= measuredApi.isEmpty ? 'null': measuredApi;

    final response = await http.get(Uri.parse('http://localhost:5000/filtro/${location.latitude}/${location.longitude}/${location.latitude}/${location.longitude}/$agent/$expressedInApi/$measuredApi'));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final measurements = _processMeasurements(data);
      final measurementsMedia = _mediaMeasurements(data);

      completer.complete(); // Completa o FutureBuilder para exibir o AlertDialog com os dados

      if (completer.isCompleted) {
        Navigator.of(context).pop();
        showDialog(

          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: const Text('Coordenada'),
              content:SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    PieChartWithLegend(measurements: measurementsMedia),

                    Text('Latitude: ${location.latitude}\nLongitude: ${location.longitude}'),
                    const SizedBox(height: 16),
                    Text('Media de Dados da API:'),
                    for (var measurement in measurementsMedia)
                      Text(
                        'Tipo de qualidade medida: ${measurement.measured}\n'
                            'Valor: ${measurement.hasQualityValue}\n',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    Text('Lista de medições'),
                    const SizedBox(height: 16),
                    Text('Dados da API:'),
                    for (var measurement in measurements)
                      Text(
                        'Tipo de qualidade medida: ${measurement.measured}\n'
                            'Unidade: ${measurement.expressedIn}\n'
                            'Valor: ${measurement.hasQualityValue}\n'
                            'Data de início: ${measurement.hasBeginPointInXSDDateTimeStamp}\n',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                  ],
                )
              ),
              actions: [
                TextButton(
                  child: const Text('Fechar'),
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                ),
              ],
            );
          },
        );
      }
    } else {
      completer.complete(); // Completa o FutureBuilder mesmo em caso de erro

      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('Erro'),
            content: const Text('Erro ao obter os dados da API.'),
            actions: [
              TextButton(
                child: const Text('Fechar'),
                onPressed: () {
                  Navigator.of(context).pop();
                },
              ),
            ],
          );
        },
      );
    }
  }

  List<Measurement> _mediaMeasurements(dynamic data) {
    final Map<String, List<double>> measuredValuesMap = {};

    for (var locationData in data) {
      for (var resultData in locationData['results']) {
        for (var measuredQualityKindData in resultData['measuredQualityKind']) {
          final measured = measuredQualityKindData['measured'];
          final hasQualityValueData = measuredQualityKindData['hasQualityValue'];

          final hasQualityValueList = measuredValuesMap.putIfAbsent(measured, () => []);

          if (hasQualityValueData is String) {
            final hasQualityValue = double.tryParse(hasQualityValueData) ?? 0.0;
            hasQualityValueList.add(hasQualityValue);
          } else if (hasQualityValueData is Iterable) {
            for (var value in hasQualityValueData) {
              if (value is String) {
                final hasQualityValue = double.tryParse(value) ?? 0.0;
                hasQualityValueList.add(hasQualityValue);
              }
            }
          }
        }
      }
    }

    final List<Measurement> measurements = [];

    measuredValuesMap.forEach((measured, hasQualityValueList) {
      final double averageQualityValue = hasQualityValueList.isNotEmpty
          ? hasQualityValueList.reduce((a, b) => a + b) / hasQualityValueList.length
          : 0.0;

      final measurement = Measurement(
        measured: measured,
        expressedIn: '',
        hasQualityValue: averageQualityValue,
        hasBeginPointInXSDDateTimeStamp: '',
      );

      measurements.add(measurement);
    });

    return measurements;
  }


  List<Measurement> _processMeasurements(dynamic data) {
    final List<Measurement> measurements = [];

    for (var locationData in data) {
      final lat = locationData['lat'];
      final long = locationData['long'];

      for (var resultData in locationData['results']) {
        final subject = resultData['subject'];

        for (var measuredQualityKindData in resultData['measuredQualityKind']) {
          final expressedIn = measuredQualityKindData['expressedIn'];
          final measured = measuredQualityKindData['measured'];
          final hasBeginPointInXSDDateTimeStamp =
          measuredQualityKindData['hasBeginPointInXSDDateTimeStamp'];

          for (var participatedInData in resultData['participatedIn']) {
            final agent = participatedInData['agent'];

            final hasQualityValueList = [];
            final hasQualityValueData =
            measuredQualityKindData['hasQualityValue'];

            if (hasQualityValueData is String) {
              final hasQualityValue =
                  double.tryParse(hasQualityValueData) ?? 0.0;
              hasQualityValueList.add(hasQualityValue);
            } else if (hasQualityValueData is Iterable) {
              for (var value in hasQualityValueData) {
                if (value is String) {
                  final hasQualityValue =
                      double.tryParse(value) ?? 0.0;
                  hasQualityValueList.add(hasQualityValue);
                }
              }
            }

            final averageQualityValue =
                hasQualityValueList.reduce((a, b) => a + b) /
                    hasQualityValueList.length;

            final measurement = Measurement(
              measured: measured,
              expressedIn: expressedIn,
              hasQualityValue: averageQualityValue,
              hasBeginPointInXSDDateTimeStamp: hasBeginPointInXSDDateTimeStamp,
            );

            measurements.add(measurement);
          }
        }
      }
    }

    return measurements;
  }



  void _resetZoom() {
    _mapController.move(_markerLocation, 8);
    _fetchLocations();
    _fetchData();

    build(context);

  }


}

const List<String> list = <String>['','One', 'Two', 'Three', 'Four'];



class DropdownMenuExample extends StatefulWidget {
  const DropdownMenuExample({super.key});

  @override
  State<DropdownMenuExample> createState() => _DropdownMenuExampleState();
}

class DropdownUnidadedeMedida extends StatefulWidget {

  const DropdownUnidadedeMedida({super.key});

  @override
  State<DropdownUnidadedeMedida> createState() => _DropdownMenuUnidadedeMedida();
}
class DropdownQualidadeMedida extends StatefulWidget {

  const DropdownQualidadeMedida({super.key});

  @override
  State<DropdownQualidadeMedida> createState() => _DropdownMenuQualidadeMedida();
}

class _DropdownMenuExampleState extends State<DropdownMenuExample> {
  String dropdownValue = agent;

  @override
  Widget build(BuildContext context) {
    return DropdownMenu<String>(
      initialSelection: agent,
      width: 260,
      enableFilter: true,
      label: const Text('AGENTE RESPONSAVEL'),
      onSelected: (String? value) {
        // This is called when the user selects an item.
        setState(() {
          dropdownValue = value!;
          agent =  value!;
        });
      },
      dropdownMenuEntries: participatedIn.map<DropdownMenuEntry<String>>((String value) {
        return DropdownMenuEntry<String>(value: value, label: value);
      }).toList(),
    );
  }
}


class _DropdownMenuUnidadedeMedida extends State<DropdownUnidadedeMedida> {
  String dropdownValue = expressedInApi;

  @override
  Widget build(BuildContext context) {

    return DropdownMenu<String>(
      initialSelection: expressedInApi,
      width: 260,
      enableFilter: true,
      label: const Text('Unidade de Medida'),
      onSelected: (String? value) {
        // This is called when the user selects an item.
        setState(() {
          dropdownValue = value!;
          expressedInApi = value!;
        });
      },
      dropdownMenuEntries: expressedIn.map<DropdownMenuEntry<String>>((String value) {
        return DropdownMenuEntry<String>(value: value, label: value);
      }).toList(),
    );
  }
}




class _DropdownMenuQualidadeMedida extends State<DropdownQualidadeMedida> {
  String dropdownValue = measuredApi;

  @override
  Widget build(BuildContext context) {

    return DropdownMenu<String>(
      initialSelection:measuredApi ,
      width: 260,
      enableFilter: true,
      label: const Text('Qualidade Medida'),
      onSelected: (String? value) {
        // This is called when the user selects an item.
        setState(() {
          dropdownValue = value!;
          measuredApi = value!;
        });
      },
      dropdownMenuEntries: measured.map<DropdownMenuEntry<String>>((String value) {
        return DropdownMenuEntry<String>(value: value, label: value);
      }).toList(),
    );
  }
}


