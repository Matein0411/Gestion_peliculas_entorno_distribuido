import React, { useState } from 'react';
import Header from './components/Header';
import DatabaseButton from './components/DatabaseButton';
import ResultsPanel from './components/ResultsPanel';
import NodeStatus from './components/NodeStatus';
import TablaEmpleados from './components/TablaEmpleados';
import TablaPromociones from './components/TablaPromociones';
import TablaClientes from './components/TablaClientes';
import TablaPeliculas from './components/TablaPeliculas';


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
  const [promocionesAntes, setPromocionesAntes] = useState<any[]>([]);
  const [promocionesDespues, setPromocionesDespues] = useState<any[]>([]);
  const [vistaActual, setVistaActual] = useState<"empleados" | "promociones" | "clientes" | "peliculas" | null>(null);
  const [clientes, setClientes] = useState<any[]>([]);
  const [clientesCargados, setClientesCargados] = useState(false);
  const [peliculasCuencaAntes, setPeliculasCuencaAntes] = useState<any[]>([]);
  const [peliculasCuencaDespues, setPeliculasCuencaDespues] = useState<any[]>([]);


  const [mostrarTablas, setMostrarTablas] = useState(false);

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
    const handleFragmentacionHorizontal = async () => {
     if (!clientesCargados) {
      addOperation(
        'Fragmentación Horizontal',
        'Fragmentación de la tabla clientes por ciudad',
        'Clientes Quito → Nodo Quito\nClientes Guayaquil → Nodo Guayaquil\nClientes Cuenca → Nodo Cuenca'
      );
      setClientesCargados(true);
    }
   setEmpleados([]);
   setEmpleadosCargados(false); 

   try {
     const response = await fetch('http://localhost:8000/api/v1/clientes-unificados');
     if (!response.ok) throw new Error('Error en la respuesta del servidor');
     const data = await response.json();
     setClientes(data);
    }catch (error) {
    console.error('❌ Error al obtener clientes:', error);
    }
    setVistaActual("clientes");
    setMostrarTablas(false);
    setEmpleados([]); // opcional si deseas limpiar empleados al cambiar de vista
   };

// Fragmentación vertical
      const handleFragmentacionVertical = async () => {
    if(!empleadosCargados){
      addOperation(
      'Fragmentación Vertical',
      'Fragmentación de la tabla empleados por atributos',
      'Guayaquil: id, nombre, apellido, cargo \Quito: ciudad, salario, fecha contratación, contacto emergencia'
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

    setVistaActual("empleados");
    setMostrarTablas(false); // Oculta las promociones si estaban visibles

  };



const handleReplicacion = async (origen: string, destino: string) => {
  try {
    const cantidadRegistros = 1;
    const response = await fetch(`http://localhost:8000/api/v1/replicacion-bidireccional?nodo_para_insertar=${origen}&cantidad_registros=${cantidadRegistros}`, {
      method: "POST"
    });

    if (!response.ok) throw new Error("Fallo en la replicación");

    const resultado = await response.json();
    const antes = resultado.evidencia_replicacion_bidireccional["1_estado_antes"];
    const despues = resultado.evidencia_replicacion_bidireccional["3_estado_despues"];

    setPromocionesAntes(antes[`promociones_${origen.toLowerCase()}`]);
    setPromocionesDespues(despues[`promociones_${origen.toLowerCase()}`]);
    setMostrarTablas(true);
    setVistaActual("promociones");
    setEmpleados([]);

    // ✅ Lógica para mostrar si es bidireccional o unidireccional
    const esBidireccional = 
      (origen === "Guayaquil" && destino === "Quito") || 
      (origen === "Quito" && destino === "Guayaquil");

    const tipo = esBidireccional ? "Replicación Bidireccional" : "Replicación Unidireccional";
    const descripcion = esBidireccional 
      ? `Replicación de promociones entre ${origen} y ${destino}` 
      : `Replicación de promociones desde ${origen} hacia ${destino}`;

    const detalles = `Nodo origen: ${origen} → Nodo destino: ${destino}`;

    addOperation(tipo, descripcion, detalles);

  } catch (error) {
    console.error("❌ Error en replicación:", error);
  }
};

//peliculas replicadas quito cuenca
const handleReplicacionUnidireccionalQuitoCuenca = async () => {
  try {
    const cantidad = 1; // siempre será 1 como pediste
    const response = await fetch(`http://localhost:8000/api/v1/replicacion-unidireccional/quito-cuenca?cantidad=${cantidad}`, {
      method: 'POST'
    });

    if (!response.ok) throw new Error("Error en la replicación Quito → Cuenca");

    const data = await response.json();

    // Extraer estado antes y después para Cuenca
    const antes = data.tablas_antes.cuenca_peliculas;
    const despues = data.tablas_despues.cuenca_peliculas;

    setPeliculasCuencaAntes(antes);
    setPeliculasCuencaDespues(despues);
    setVistaActual("peliculas");
    setMostrarTablas(true);

    addOperation(
      "Replicación Unidireccional",
      "Replicación de películas de Quito a Cuenca",
      "Nodo origen: Quito → Nodo destino: Cuenca"
    );
  } catch (error) {
    console.error("❌ Error replicando Quito → Cuenca:", error);
  }
};

// replicación unidireccional Guayaquil → Cuenca
const handleReplicacionUnidireccionalGuayaquilCuenca = async () => {
  try {
    const cantidad = 1; // igual que en el otro caso
    const response = await fetch(`http://localhost:8000/api/v1/replicacion-unidireccional/guayaquil-cuenca?cantidad=${cantidad}`, {
      method: 'POST'
    });

    if (!response.ok) throw new Error("Error en la replicación Guayaquil → Cuenca");

    const data = await response.json();

    // Extraer estado antes y después para Cuenca
    const antes = data.tablas_antes.cuenca_peliculas;
    const despues = data.tablas_despues.cuenca_peliculas;

    setPeliculasCuencaAntes(antes);
    setPeliculasCuencaDespues(despues);
    setVistaActual("peliculas");
    setMostrarTablas(true);

    addOperation(
      "Replicación Unidireccional",
      "Replicación de películas de Guayaquil a Cuenca",
      "Nodo origen: Guayaquil → Nodo destino: Cuenca"
    );
  } catch (error) {
    console.error("❌ Error replicando Guayaquil → Cuenca:", error);
  }
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
              description="Distribución de atributos entre Guayaquil y Quito"
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
              title="Alquiler: Cuenca → Quito"
              description="Replicación unidireccional de tabla Alquiler: Cuenca a Quito"
              icon={ArrowRight}
              onClick={() => handleReplicacion('Cuenca', 'Quito')}
              variant="replication"
            />

            <DatabaseButton
              title="Alquiler: Cuenca → Guayaquil"
              description="Replicación unidireccional de tabla Alquiler: Cuenca a Guayaquil"
              icon={ArrowRight}
              onClick={() => handleReplicacion('Cuenca', 'Guayaquil')}
              variant="replication"
            />

            {/* Alquiler: Quito → Cuenca / Guayaquil → Cuenca */}
            <DatabaseButton
              title="Peliculas_Catalogo: Quito → Cuenca"
              description="Replicación unidireccional de tabla Peliculas_Catalogo: Quito a Cuenca"
              icon={ArrowRight}
              onClick={handleReplicacionUnidireccionalQuitoCuenca} // ✅ CORRECTO
              variant="replication"
            />



            <DatabaseButton
              title="Peliculas_Catalogo: Guayaquil → Cuenca"
              description="Replicación unidireccional de tabla Peliculas_Catalogo: Guayaquil a Cuenca"
              icon={ArrowRight}
              onClick={handleReplicacionUnidireccionalGuayaquilCuenca}
              variant="replication"
            />


          </div>
        </div>

        {/* Panel de Resultados */}
        <ResultsPanel operations={operations} isVisible={showResults} />
        
        {vistaActual === "empleados" && empleados.length > 0 && (
          <TablaEmpleados empleados={empleados} />
        )}

        {vistaActual === "promociones" && mostrarTablas && (
          <>
            <TablaPromociones titulo="ANTES" promociones={promocionesAntes} />
            <TablaPromociones titulo="DESPUÉS" promociones={promocionesDespues} />
          </>
        )}

        {vistaActual === "clientes" && clientes.length > 0 && (
          <TablaClientes clientes={clientes} />
        )}

        {vistaActual === "peliculas" && mostrarTablas && (
        <>
          <TablaPeliculas titulo="ANTES (Cuenca)" peliculas={peliculasCuencaAntes} />
          <TablaPeliculas titulo="DESPUÉS (Cuenca)" peliculas={peliculasCuencaDespues} />
        </>
        )}


      </main>
      
    </div>
  );
}

export default App;