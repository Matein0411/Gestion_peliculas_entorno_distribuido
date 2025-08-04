import React from 'react';

interface Cliente {
  cliente_id: string;
  nombre: string;
  apellido: string;
  email: string;
  telefono: string | null;
  direccion: string | null;
  ciudad_registro: string;
  fecha_creacion: string;
}

interface Props {
  clientes: Cliente[];
}

const TablaClientes: React.FC<Props> = ({ clientes }) => {
  return (
    <div className="overflow-x-auto mt-6 shadow-lg rounded-lg border border-gray-200 bg-white">
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-blue-100 text-blue-800 font-semibold">
          <tr>
            <th className="px-4 py-2">ID</th>
            <th className="px-4 py-2">Nombre</th>
            <th className="px-4 py-2">Apellido</th>
            <th className="px-4 py-2">Email</th>
            <th className="px-4 py-2">Teléfono</th>
            <th className="px-4 py-2">Dirección</th>
            <th className="px-4 py-2">Ciudad</th>
            <th className="px-4 py-2">Fecha de creación</th>
          </tr>
        </thead>
        <tbody>
          {clientes.map((cliente) => (
            <tr key={`${cliente.cliente_id}-${cliente.email}`} className="divide-y divide-gray-100">
              <td className="px-4 py-2">{cliente.cliente_id}</td>
              <td className="px-4 py-2">{cliente.nombre}</td>
              <td className="px-4 py-2">{cliente.apellido}</td>
              <td className="px-4 py-2">{cliente.email}</td>
              <td className="px-4 py-2">{cliente.telefono || 'N/A'}</td>
              <td className="px-4 py-2">{cliente.direccion || 'N/A'}</td>
              <td className="px-4 py-2">{cliente.ciudad_registro}</td>
              <td className="px-4 py-2">{new Date(cliente.fecha_creacion).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TablaClientes;