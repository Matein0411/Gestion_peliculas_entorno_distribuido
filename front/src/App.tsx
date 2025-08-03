import React, { useState } from 'react';
import Header from './components/Header';
import DatabaseButton from './components/DatabaseButton';
import ResultsPanel from './components/ResultsPanel';
import NodeStatus from './components/NodeStatus';
import { 
  Split, 
  Columns, 
  ArrowRight, 
  Copy, 
  RefreshCw 
} from 'lucide-react';

interface Operation {
  id: string;
  type: string;
  description: string;
  status: 'completed' | 'running' | 'pending';
  timestamp: string;
  details?: string;
}

interface Node {
  id: string;
  name: string;
  status: 'online' | 'offline' | 'syncing';
  dbms: string;
  records: number;
}

function App() {
  const [operations, setOperations] = useState<Operation[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [nodes, setNodes] = useState<Node[]>([
    { id: 'quito', name: 'Quito', status: 'online', dbms: 'PostgreSQL 17', records: 1250 },
    { id: 'guayaquil', name: 'Guayaquil', status: 'online', dbms: 'PostgreSQL 17', records: 1250 },
    { id: 'cuenca', name: 'Cuenca', status: 'online', dbms: 'Oracle 21c', records: 1250 }
  ]);


  const addOperation = (type: string, description: string, details?: string) => {
    const newOperation: Operation = {
      id: Date.now().toString(),
      type,
      description,
      status: 'running',
      timestamp: new Date().toLocaleTimeString(),
      details
    };

    setOperations(prev => [newOperation, ...prev]);
    setShowResults(true);

    // Simular completación después de 2 segundos
    setTimeout(() => {
      setOperations(prev => 
        prev.map(op => 
          op.id === newOperation.id 
            ? { ...op, status: 'completed' as const }
            : op
        )
      );
    }, 2000);
  };

  const handleFragmentacionHorizontal = () => {
    addOperation(
      'Fragmentación Horizontal',
      'Fragmentando tabla PELICULAS por año de lanzamiento',
      'Fragmento 1: películas 2020-2025 → SO1\nFragmento 2: películas 2015-2019 → SO2\nFragmento 3: películas 2010-2014 → SO3'
    );
  };

  const handleFragmentacionVertical = () => {
    addOperation(
      'Fragmentación Vertical',
      'Fragmentando tabla CLIENTES por atributos',
      'Fragmento 1: id, nombre, email → SO1\nFragmento 2: id, telefono, direccion → SO2\nFragmento 3: id, fecha_registro, preferencias → SO3'
    );
  };

  const handleReplicacion = (origen: string, destino: string) => {
    const sourceNode = nodes.find(n => n.name === origen);
    const targetNode = nodes.find(n => n.name === destino);
    
    addOperation(
      `Réplica ${origen} a ${destino}`,
      `Replicando datos desde ${origen} (${sourceNode?.dbms}) hacia ${destino} (${targetNode?.dbms})`,
      `Sincronizando tablas: PELICULAS, CLIENTES, ALQUILERES\nRegistros replicados: ${sourceNode?.records || 0}`
    );

    // Simular sincronización de nodos
    setNodes(prev => prev.map(node => {
      if (node.name === destino) {
        return { ...node, status: 'syncing' as const };
      }
      return node;
    }));

    setTimeout(() => {
      setNodes(prev => prev.map(node => {
        if (node.name === destino) {
          return { ...node, status: 'online' as const, records: sourceNode?.records || node.records };
        }
        return node;
      }));
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {/* Estado de Nodos */}
        <NodeStatus nodes={nodes} />

        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-medium mb-4">
            <RefreshCw className="h-4 w-4" />
            <span>Sistema Activo - 3 Nodos Conectados</span>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Panel de Control de Base de Datos Distribuida
          </h2>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Gestiona la fragmentación y replicación de datos entre los nodos del sistema de alquiler de películas.
          </p>
        </div>

        {/* Fragmentación Section */}
        <div className="mb-12">
          <div className="flex items-center space-x-3 mb-6">
            <Split className="h-6 w-6 text-emerald-600" />
            <h3 className="text-2xl font-bold text-gray-900">Fragmentación de Datos</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <DatabaseButton
              title="Fragmentación Horizontal"
              description="Divide las tablas por filas según criterios específicos (ej: año de película)"
              icon={Split}
              onClick={handleFragmentacionHorizontal}
              variant="fragmentation"
            />
            
            <DatabaseButton
              title="Fragmentación Vertical"
              description="Divide las tablas por columnas distribuyendo atributos entre nodos"
              icon={Columns}
              onClick={handleFragmentacionVertical}
              variant="fragmentation"
            />
          </div>
        </div>

        {/* Replicación Section */}
        <div className="mb-12">
          <div className="flex items-center space-x-3 mb-6">
            <Copy className="h-6 w-6 text-blue-600" />
            <h3 className="text-2xl font-bold text-gray-900">Replicación de Datos</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <DatabaseButton
              title="Réplica SO1 a SO2"
              description="Replica datos desde PostgreSQL SO1 hacia PostgreSQL SO2"
              icon={ArrowRight}
              onClick={() => handleReplicacion('SO1', 'SO2')}
              variant="replication"
            />
            
            <DatabaseButton
              title="Réplica SO1 a SO3"
              description="Replica datos desde PostgreSQL SO1 hacia Oracle SO3"
              icon={ArrowRight}
              onClick={() => handleReplicacion('SO1', 'SO3')}
              variant="replication"
            />
            
            <DatabaseButton
              title="Réplica SO2 a SO1"
              description="Replica datos desde PostgreSQL SO2 hacia PostgreSQL SO1"
              icon={ArrowRight}
              onClick={() => handleReplicacion('SO2', 'SO1')}
              variant="replication"
            />
            
            <DatabaseButton
              title="Réplica SO2 a SO3"
              description="Replica datos desde PostgreSQL SO2 hacia Oracle SO3"
              icon={ArrowRight}
              onClick={() => handleReplicacion('SO2', 'SO3')}
              variant="replication"
            />
            
            <DatabaseButton
              title="Réplica SO3 a SO1"
              description="Replica datos desde Oracle SO3 hacia PostgreSQL SO1"
              icon={ArrowRight}
              onClick={() => handleReplicacion('SO3', 'SO1')}
              variant="replication"
            />
            
            <DatabaseButton
              title="Réplica SO3 a SO2"
              description="Replica datos desde Oracle SO3 hacia PostgreSQL SO2"
              icon={ArrowRight}
              onClick={() => handleReplicacion('SO3', 'SO2')}
              variant="replication"
            />
          </div>
        </div>

        {/* Panel de Resultados */}
        <ResultsPanel operations={operations} isVisible={showResults} />
      </main>
    </div>
  );
}

export default App;