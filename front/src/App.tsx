import React, { useState } from 'react';
import Header from './components/Header';
import DatabaseButton from './components/DatabaseButton';
import ResultsPanel from './components/ResultsPanel';
import NodeStatus from './components/NodeStatus';
import TablaEmpleados from './components/TablaEmpleados';

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
  console.log("App cargada");

  const [operations, setOperations] = useState<Operation[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [empleadosCargados, setEmpleadosCargados] = useState(false);
  const [empleados, setEmpleados] = useState<any[]>([]);
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

// Fragmentación horizontal Datos
    const handleFragmentacionHorizontal = () => {
      addOperation(
        'Fragmentación Horizontal',
        'Fragmentación de la tabla clientes por ciudad',
        'Clientes Quito → Nodo Quito\nClientes Guayaquil → Nodo Guayaquil\nClientes Cuenca → Nodo Cuenca'
      );
    };

// Fragmentación vertical
      const handleFragmentacionVertical = async () => {
    if(!empleadosCargados){
      addOperation(
      'Fragmentación Vertical',
      'Fragmentación de la tabla empleados por atributos',
      'Guayaquil: id, nombre, apellido, cargo \nCuenca: ciudad, salario, fecha contratación, contacto emergencia'
    );
    setEmpleadosCargados(true);
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/empleados-vista-completa');
      if (!response.ok) throw new Error('Error en la respuesta del servidor');
      const data = await response.json();
      setEmpleados(data);
    } catch (error) {
      console.error('❌ Error al obtener empleados:', error);
    }
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
            {/* botones fragmentación Horizontal y Vertical */}
            <DatabaseButton
              title="Clientes (Fragmentación Horizontal)"
              description="Distribución por ciudad: Quito, Guayaquil y Cuenca"
              icon={Split}
              onClick={handleFragmentacionHorizontal}
              variant="fragmentation"
            />
            <DatabaseButton
              title="Empleados (Fragmentación Vertical)"
              description="Distribución de atributos entre Guayaquil y Cuenca"
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

          {/* Nombre de los botones */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {/* Promociones: Bidireccional */}
            <DatabaseButton
              title="Promociones: Guayaquil → Quito"
              description="Replicación bidireccional de tabla promociones: Guayaquil a Quito"
              icon={ArrowRight}
              onClick={() => handleReplicacion('Guayaquil', 'Quito')}
              variant="replication"
            />

            <DatabaseButton
              title="Promociones: Quito → Guayaquil"
              description="Replicación bidireccional de tabla promociones: Quito a Guayaquil"
              icon={ArrowRight}
              onClick={() => handleReplicacion('Quito', 'Guayaquil')}
              variant="replication"
            />

            {/* Catálogo: Cuenca → Quito / Guayaquil */}
            <DatabaseButton
              title="Catálogo: Cuenca → Quito"
              description="Replicación unidireccional de tabla catálogo: Cuenca a Quito"
              icon={ArrowRight}
              onClick={() => handleReplicacion('Cuenca', 'Quito')}
              variant="replication"
            />

            <DatabaseButton
              title="Catálogo: Cuenca → Guayaquil"
              description="Replicación unidireccional de tabla catálogo: Cuenca a Guayaquil"
              icon={ArrowRight}
              onClick={() => handleReplicacion('Cuenca', 'Guayaquil')}
              variant="replication"
            />

            {/* Alquiler: Quito → Cuenca / Guayaquil → Cuenca */}
            <DatabaseButton
              title="Alquiler: Quito → Cuenca"
              description="Replicación unidireccional de tabla alquiler: Quito a Cuenca"
              icon={ArrowRight}
              onClick={() => handleReplicacion('Quito', 'Cuenca')}
              variant="replication"
            />

            <DatabaseButton
              title="Alquiler: Guayaquil → Cuenca"
              description="Replicación unidireccional de tabla alquiler: Guayaquil a Cuenca"
              icon={ArrowRight}
              onClick={() => handleReplicacion('Guayaquil', 'Cuenca')}
              variant="replication"
            />

          </div>
        </div>

        {/* Panel de Resultados */}
        <ResultsPanel operations={operations} isVisible={showResults} />
        {empleados.length > 0 && (
  <TablaEmpleados empleados={empleados} />
)}
      </main>
      
    </div>
  );
}

export default App;