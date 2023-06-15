from itertools import groupby
from xml.etree.ElementTree import tostring
from flask import Flask, jsonify, request
from flask_compress import Compress
from rdflib.namespace import RDF
from rdflib import Graph, Literal, RDF, RDFS, URIRef, OWL, Namespace
import pyopencl as cl

# Configurar OpenCL para usar a placa de vídeo RX5500XT
platform = cl.get_platforms()[0]
device = platform.get_devices(device_type=cl.device_type.GPU)[0]
context = cl.Context(devices=[device])

app = Flask(__name__)
compress = Compress(app)

print("inicializando")
qualidade = []
exampleTriple = Graph()
exampleTriple.parse("integrado2.ttl", format="ttl")

doce = URIRef("http://purl.org/nemo/doce#")
DOCE = Namespace(doce)
ex = URIRef("http://purl.org/nemo/integradoce#")
DOCEEX = Namespace(ex)
wgs = URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#")
WGS = Namespace(wgs)
owl = URIRef("http://www.w3.org/2002/07/owl#")
OWL = Namespace(owl)
gufo = URIRef("http://purl.org/nemo/gufo#")
GUFO = Namespace(gufo)
xsd = URIRef("http://www.w3.org/2001/XMLSchema#")
XSD = Namespace(xsd)

print("Fim Inicialização")




app = Flask(__name__)

# Dados de exemplo
measurements_data = [
 
]

@app.route('/measurements/by_agent/<agent>', methods=['GET'])
def get_measurements_by_agent(agent):
    
    
       
    location =[]
    for s, p, o in exampleTriple.triples((None, None, DOCE.GeographicPoint)):
        results = []
        controle = True
        lat = exampleTriple.value(s, WGS.lat)
        long = exampleTriple.value(s, WGS.long)
        if lat!= None:
            lat = float(str(exampleTriple.value(s, WGS.lat)))
            long = float(str(exampleTriple.value(s, WGS.long)))
        
        
        
        

        
        
        if long != None:
            
            for s2, p2, o2 in exampleTriple.triples((None, DOCE.locatedIn,s )):
                
                
                for s3, p3, o3 in exampleTriple.triples((s2, RDF.type, DOCE.Measurement)) :
                    participatedIn = []
                    measuredQualityKind = []
                    measurement = {
                    "subject": str(s3).removeprefix("http://purl.org/nemo/integradoce#"),
                    #"predicate": str(p3),
                    #"object": str(o3),
                    "participatedIn": participatedIn,
                    "measuredQualityKind":measuredQualityKind
                    
                    }
                    for s4, p4, o4 in exampleTriple.triples((None, GUFO.participatedIn, s3)) :
                        participatedIn_dic = {
                            "agent": str(s4).removeprefix("http://purl.org/nemo/integradoce#Integradoce"),
                        }
                        if  str(agent).lower() in str(s4).lower():
                            controle = True
                        else:
                            controle = False
                            break
                        
                        participatedIn.append(participatedIn_dic)
                    if not controle:
                        continue
                    
                    for s4, p4, o4 in exampleTriple.triples((s3, DOCE.measuredQualityKind, None)) :
                        expressedIn = "" 
                        measured = []
                        hasQualityValue = []
                        hasBeginPointInXSDDateTimeStamp = ""
                        for s5, p5, o5 in exampleTriple.triples((s3, DOCE.expressedIn, None)) :
                            expressedIn_dic =  str(o5).removeprefix("http://qudt.org/vocab/unit/")
                            
                            
                            expressedIn = (expressedIn_dic)
                        for s5, p5, o5 in exampleTriple.triples((s3, DOCE.measuredQualityKind, None)) :
                            measured_dic = str(o5).removeprefix("http://purl.org/nemo/doce#")
                        
                            measured = (measured_dic)
                        for s5, p5, o5 in exampleTriple.triples((s3, GUFO.hasQualityValue, None)) :
                            hasQualityValue_dic =  str(o5)
                            
                            hasQualityValue = (hasQualityValue_dic)
                        for s5, p5, o5 in exampleTriple.triples((s3, GUFO.hasBeginPointInXSDDateTimeStamp, None)) :
                            hasBeginPointInXSDDateTimeStamp_dic = str(o5)
                            
                            hasBeginPointInXSDDateTimeStamp = (hasBeginPointInXSDDateTimeStamp_dic)
                        measuredQualityKind_dic = {
                            
                            "expressedIn": expressedIn,
                            "measured":measured, 
                            "hasQualityValue":hasQualityValue,
                            "hasBeginPointInXSDDateTimeStamp":hasBeginPointInXSDDateTimeStamp 
                            
                        }
                        measuredQualityKind.append(measuredQualityKind_dic)
                    
                
                if not controle:
                    continue
                
                results.append(measurement)
            
            if  len(results)>=1:
                location.append({
                "lat":lat,
                "long": long,
                "results": results
            })
        
        
    return location



@app.route('/measurements/by_time_interval', methods=['GET'])
def get_measurements_by_time_interval():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    results = [m for m in measurements_data if start_date <= m['timestamp'] <= end_date]
    return jsonify(results)

@app.route('/points', methods=['GET'])
def get_geographic_point():
    
    location =[]
    for s, p, o in exampleTriple.triples((None, None, DOCE.GeographicPoint)):
        results = []
        lat = exampleTriple.value(s, WGS.lat)
        long = exampleTriple.value(s, WGS.long)
        #print(lat)
        #print(long)
        
        
        
        for s2, p2, o2 in exampleTriple.triples((None, DOCE.locatedIn,s )):
            
            
            for s3, p3, o3 in exampleTriple.triples((s2, RDF.type, DOCE.Measurement)) :
                participatedIn = []
                measuredQualityKind = []
                measurement = {
                "subject": str(s3).removeprefix("http://purl.org/nemo/integradoce#"),
                #"predicate": str(p3),
                #"object": str(o3),
                "participatedIn": participatedIn,
                "measuredQualityKind":measuredQualityKind
                
                }
                for s4, p4, o4 in exampleTriple.triples((None, GUFO.participatedIn, s3)) :
                    participatedIn_dic = {
                        "agent": str(s4).removeprefix("http://purl.org/nemo/integradoce#Integradoce"),
                    }
                    participatedIn.append(participatedIn_dic)
                for s4, p4, o4 in exampleTriple.triples((s3, DOCE.measuredQualityKind, None)) :
                    expressedIn = "" 
                    measured = []
                    hasQualityValue = []
                    hasBeginPointInXSDDateTimeStamp = ""
                    for s5, p5, o5 in exampleTriple.triples((s3, DOCE.expressedIn, None)) :
                        expressedIn_dic =  str(o5).removeprefix("http://qudt.org/vocab/unit/")
                        
                        
                        expressedIn = (expressedIn_dic)
                    for s5, p5, o5 in exampleTriple.triples((s3, DOCE.measuredQualityKind, None)) :
                        measured_dic = str(o5).removeprefix("http://purl.org/nemo/doce#")
                    
                        measured = (measured_dic)
                    for s5, p5, o5 in exampleTriple.triples((s3, GUFO.hasQualityValue, None)) :
                        hasQualityValue_dic =  str(o5)
                        
                        hasQualityValue = (hasQualityValue_dic)
                    for s5, p5, o5 in exampleTriple.triples((s3, GUFO.hasBeginPointInXSDDateTimeStamp, None)) :
                        hasBeginPointInXSDDateTimeStamp_dic = str(o5)
                        
                        hasBeginPointInXSDDateTimeStamp = (hasBeginPointInXSDDateTimeStamp_dic)
                    measuredQualityKind_dic = {
                        
                        "expressedIn": expressedIn,
                        "measured":measured, 
                        "hasQualityValue":hasQualityValue,
                        "hasBeginPointInXSDDateTimeStamp":hasBeginPointInXSDDateTimeStamp 
                        
                    }
                    measuredQualityKind.append(measuredQualityKind_dic)
                
            
            
            results.append(measurement)
        
        if  len(results)>=1:
            location.append({
            "lat":lat,
            "long": long,   
        })
        
        
    return  jsonify(location)

@app.route('/measurements/by_quality_kind/<quality_kind>', methods=['GET'])
def get_measurements_by_quality_kind(quality_kind):
    results = [m for m in measurements_data if m['quality_kind'] == quality_kind]
    return jsonify(results)

@app.route('/measurements', methods=['GET'])
@compress.compressed()
def get_measurements2():
    limit = int(request.args.get('limit', 10))  # Número de resultados por página, o padrão é 10
    offset = int(request.args.get('offset', 0))  # Número de resultados a serem ignorados, o padrão é 0

    # Aplicar paginação aos dados
    paginated_results = JSON[offset:offset+limit]

    # Filtrar os resultados pelo agente, se fornecido
   

    return jsonify(paginated_results)

def get_measurements():
    
    location =[]
    for s, p, o in exampleTriple.triples((None, None, DOCE.GeographicPoint)):
        results = []
        lat = exampleTriple.value(s, WGS.lat)
        long = exampleTriple.value(s, WGS.long)
        #print(lat)
        #print(long)
        
        
        
        for s2, p2, o2 in exampleTriple.triples((None, DOCE.locatedIn,s )):
            
            
            for s3, p3, o3 in exampleTriple.triples((s2, RDF.type, DOCE.Measurement)) :
                participatedIn = []
                measuredQualityKind = []
                measurement = {
                "subject": str(s3).removeprefix("http://purl.org/nemo/integradoce#"),
                #"predicate": str(p3),
                #"object": str(o3),
                "participatedIn": participatedIn,
                "measuredQualityKind":measuredQualityKind
                
                }
                for s4, p4, o4 in exampleTriple.triples((None, GUFO.participatedIn, s3)) :
                    participatedIn_dic = {
                        "agent": str(s4).removeprefix("http://purl.org/nemo/integradoce#Integradoce"),
                    }
                    participatedIn.append(participatedIn_dic)
                for s4, p4, o4 in exampleTriple.triples((s3, DOCE.measuredQualityKind, None)) :
                    expressedIn = "" 
                    measured = []
                    hasQualityValue = []
                    hasBeginPointInXSDDateTimeStamp = ""
                    for s5, p5, o5 in exampleTriple.triples((s3, DOCE.expressedIn, None)) :
                        expressedIn_dic =  str(o5).removeprefix("http://qudt.org/vocab/unit/")
                        
                        
                        expressedIn = (expressedIn_dic)
                    for s5, p5, o5 in exampleTriple.triples((s3, DOCE.measuredQualityKind, None)) :
                        measured_dic = str(o5).removeprefix("http://purl.org/nemo/doce#")
                    
                        measured = (measured_dic)
                    for s5, p5, o5 in exampleTriple.triples((s3, GUFO.hasQualityValue, None)) :
                        hasQualityValue_dic =  str(o5)
                        
                        hasQualityValue = (hasQualityValue_dic)
                    for s5, p5, o5 in exampleTriple.triples((s3, GUFO.hasBeginPointInXSDDateTimeStamp, None)) :
                        hasBeginPointInXSDDateTimeStamp_dic = str(o5)
                        
                        hasBeginPointInXSDDateTimeStamp = (hasBeginPointInXSDDateTimeStamp_dic)
                    measuredQualityKind_dic = {
                        
                        "expressedIn": expressedIn,
                        "measured":measured, 
                        "hasQualityValue":hasQualityValue,
                        "hasBeginPointInXSDDateTimeStamp":hasBeginPointInXSDDateTimeStamp 
                        
                    }
                    measuredQualityKind.append(measuredQualityKind_dic)
                
            
            
            results.append(measurement)
        
        if  len(results)>=1:
            location.append({
            "lat":lat,
            "long": long,
            "results": results
        })
        
        
    return location

JSON = get_measurements()

@app.route('/measurements/<latapi>/<longapi>/<latapi2>/<longapi2>', methods=['GET'])
def get_measurements_by_location(latapi,longapi,latapi2,longapi2):
    print(latapi,longapi)
    print(latapi2,longapi2)
    
    lat_range= []
    
    lat_range.append(float(latapi))
    lat_range.append(float(latapi2))
    
    long_range=[]
    long_range.append(float(longapi))
    long_range.append(float(longapi2))
    
    print(lat_range)
    print(long_range)
    long_range_min = min(long_range)
    
    location =[]
    for s, p, o in exampleTriple.triples((None, None, DOCE.GeographicPoint)):
        results = []
        lat = exampleTriple.value(s, WGS.lat)
        long = exampleTriple.value(s, WGS.long)
        if lat!= None:
            lat = float(str(exampleTriple.value(s, WGS.lat)))
            long = float(str(exampleTriple.value(s, WGS.long)))
        
        
        
        if long != None:
            print((lat))
            print( (long))
            print("Api:")
            print("minimo long:", (min(long_range)))
            print("maximo long:", max(long_range))
            print("minimo lat:", min(lat_range))
            print("maximo lat:", max(lat_range))

        
        
        if long != None and (((long>min(long_range) or long==min(long_range))) and ((long<max(long_range) or long==max(long_range)))) and (((lat>min(lat_range) or lat==min(lat_range))) and ((lat<max(lat_range) or lat==max(lat_range)))):
            print("validar")
            print((long<min(long_range) or long==min(long_range)))
            for s2, p2, o2 in exampleTriple.triples((None, DOCE.locatedIn,s )):
                
                
                for s3, p3, o3 in exampleTriple.triples((s2, RDF.type, DOCE.Measurement)) :
                    participatedIn = []
                    measuredQualityKind = []
                    measurement = {
                    "subject": str(s3).removeprefix("http://purl.org/nemo/integradoce#"),
                    #"predicate": str(p3),
                    #"object": str(o3),
                    "participatedIn": participatedIn,
                    "measuredQualityKind":measuredQualityKind
                    
                    }
                    for s4, p4, o4 in exampleTriple.triples((None, GUFO.participatedIn, s3)) :
                        participatedIn_dic = {
                            "agent": str(s4).removeprefix("http://purl.org/nemo/integradoce#Integradoce"),
                        }
                        
                        participatedIn.append(participatedIn_dic)
                    for s4, p4, o4 in exampleTriple.triples((s3, DOCE.measuredQualityKind, None)) :
                        expressedIn = "" 
                        measured = []
                        hasQualityValue = []
                        hasBeginPointInXSDDateTimeStamp = ""
                        for s5, p5, o5 in exampleTriple.triples((s3, DOCE.expressedIn, None)) :
                            expressedIn_dic =  str(o5).removeprefix("http://qudt.org/vocab/unit/")
                            
                            
                            expressedIn = (expressedIn_dic)
                        for s5, p5, o5 in exampleTriple.triples((s3, DOCE.measuredQualityKind, None)) :
                            measured_dic = str(o5).removeprefix("http://purl.org/nemo/doce#")
                        
                            measured = (measured_dic)
                        for s5, p5, o5 in exampleTriple.triples((s3, GUFO.hasQualityValue, None)) :
                            hasQualityValue_dic =  str(o5)
                            
                            hasQualityValue = (hasQualityValue_dic)
                        for s5, p5, o5 in exampleTriple.triples((s3, GUFO.hasBeginPointInXSDDateTimeStamp, None)) :
                            hasBeginPointInXSDDateTimeStamp_dic = str(o5)
                            
                            hasBeginPointInXSDDateTimeStamp = (hasBeginPointInXSDDateTimeStamp_dic)
                        measuredQualityKind_dic = {
                            
                            "expressedIn": expressedIn,
                            "measured":measured, 
                            "hasQualityValue":hasQualityValue,
                            "hasBeginPointInXSDDateTimeStamp":hasBeginPointInXSDDateTimeStamp 
                            
                        }
                        measuredQualityKind.append(measuredQualityKind_dic)
                    
                
                
                results.append(measurement)
            
            if  len(results)>=1:
                location.append({
                "lat":lat,
                "long": long,
                "results": results
            })
        
        
    return location

@app.route('/filtro/<latapi>/<longapi>/<latapi2>/<longapi2>/<agent>/<expressedInApi>/<measuredApi>/', methods=['GET'])
def get_filtro(latapi,longapi,latapi2,longapi2,agent,expressedInApi,measuredApi):
    
    if agent =="null":
        agent=''
        
    if measuredApi =="null":
        measuredApi=''
        
    if expressedInApi =="null":
        expressedInApi=''
        
    
   
    controle = True
    
    lat_range= []
    
    lat_range.append(float(latapi))
    lat_range.append(float(latapi2))
    
    long_range=[]
    long_range.append(float(longapi))
    long_range.append(float(longapi2))
    
    print(lat_range)
    print(long_range)
    long_range_min = min(long_range)
    
    location =[]
    for s, p, o in exampleTriple.triples((None, None, DOCE.GeographicPoint)):
        results = []
        lat = exampleTriple.value(s, WGS.lat)
        long = exampleTriple.value(s, WGS.long)
        if lat!= None:
            lat = float(str(exampleTriple.value(s, WGS.lat)))
            long = float(str(exampleTriple.value(s, WGS.long)))
        
        
        

        
        
        if long != None and (((long>min(long_range) or long==min(long_range))) and ((long<max(long_range) or long==max(long_range)))) and (((lat>min(lat_range) or lat==min(lat_range))) and ((lat<max(lat_range) or lat==max(lat_range)))):
            
            for s2, p2, o2 in exampleTriple.triples((None, DOCE.locatedIn,s )):
                
                
                for s3, p3, o3 in exampleTriple.triples((s2, RDF.type, DOCE.Measurement)) :
                    participatedIn = []
                    measuredQualityKind = []
                    measurement = {
                    "subject": str(s3).removeprefix("http://purl.org/nemo/integradoce#"),
                    #"predicate": str(p3),
                    #"object": str(o3),
                    "participatedIn": participatedIn,
                    "measuredQualityKind":measuredQualityKind
                    
                    }
                    for s4, p4, o4 in exampleTriple.triples((None, GUFO.participatedIn, s3)) :
                        participatedIn_dic = {
                            "agent": str(s4).removeprefix("http://purl.org/nemo/integradoce#Integradoce"),
                        }
                        if  str(agent).lower() in str(s4).lower():
                            controle = True
                        else:
                            controle = False
                            break
                        
                    
                        participatedIn.append(participatedIn_dic)
                    if not controle:
                        continue
                    
                    for s4, p4, o4 in exampleTriple.triples((s3, DOCE.measuredQualityKind, None)) :
                        expressedIn = "" 
                        measured = []
                        hasQualityValue = []
                        hasBeginPointInXSDDateTimeStamp = ""
                        for s5, p5, o5 in exampleTriple.triples((s3, DOCE.expressedIn, None)) :
                            expressedIn_dic =  str(o5).removeprefix("http://qudt.org/vocab/unit/")
                            
                            
                            expressedIn = (expressedIn_dic)
                        for s5, p5, o5 in exampleTriple.triples((s3, DOCE.measuredQualityKind, None)) :
                            measured_dic = str(o5).removeprefix("http://purl.org/nemo/doce#")
                            
                        
                            measured = (measured_dic)
                        for s5, p5, o5 in exampleTriple.triples((s3, GUFO.hasQualityValue, None)) :
                            hasQualityValue_dic =  str(o5)
                            
                            hasQualityValue = (hasQualityValue_dic)
                        for s5, p5, o5 in exampleTriple.triples((s3, GUFO.hasBeginPointInXSDDateTimeStamp, None)) :
                            hasBeginPointInXSDDateTimeStamp_dic = str(o5)
                            
                            hasBeginPointInXSDDateTimeStamp = (hasBeginPointInXSDDateTimeStamp_dic)
                        measuredQualityKind_dic = {
                            
                            "expressedIn": expressedIn,
                            "measured":measured, 
                            "hasQualityValue":hasQualityValue,
                            "hasBeginPointInXSDDateTimeStamp":hasBeginPointInXSDDateTimeStamp 
                            
                        }
                        
                        if (str(expressedInApi).lower() in expressedIn.lower()) and (str(measuredApi).lower() in measured.lower()) and (True) :
                            controle = True
                        else:
                            controle = False
                            break
                        measuredQualityKind.append(measuredQualityKind_dic)
                    
                
                if not controle:
                    continue
                results.append(measurement)
            
            if  len(results)>=1:
                location.append({
                "lat":lat,
                "long": long,
                "results": results
            })
        
        
    return location


if __name__ == '__main__':
    app.run(debug=False,host='192.168.1.6')
