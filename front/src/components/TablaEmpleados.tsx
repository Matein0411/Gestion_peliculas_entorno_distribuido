import React from 'react';

interface Empleado {
  empleado_id: number;
  nombre: string;
  apellido: string;
  cargo: string;
  ciudad_tienda: string;
  salario: number;
  fecha_contratacion: string;
  contacto_emergencia: string;
}

interface TablaEmpleadosProps {
  empleados: Empleado[];
}

const TablaEmpleados: React.FC<TablaEmpleadosProps> = ({ empleados }) => {
  return (
    <div className="overflow-x-auto mt-6 shadow-lg rounded-lg border border-gray-200 bg-white">
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-blue-100 text-blue-800 font-semibold">
          <tr>
            <th className="px-4 py-2">ID</th>
            <th className="px-4 py-2">Nombre</th>
            <th className="px-4 py-2">Apellido</th>
            <th className="px-4 py-2">Cargo</th>
            <th className="px-4 py-2">Ciudad</th>
            <th className="px-4 py-2">Salario</th>
            <th className="px-4 py-2">Fecha Contratación</th>
            <th className="px-4 py-2">Contacto Emergencia</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {empleados.map((emp) => (
            <tr key={emp.empleado_id}>
              <td className="px-4 py-2">{emp.empleado_id}</td>
              <td className="px-4 py-2">{emp.nombre}</td>
              <td className="px-4 py-2">{emp.apellido}</td>
              <td className="px-4 py-2">{emp.cargo}</td>
              <td className="px-4 py-2">{emp.ciudad_tienda}</td>
              <td className="px-4 py-2">${emp.salario.toFixed(2)}</td>
              <td className="px-4 py-2">{emp.fecha_contratacion}</td>
              <td className="px-4 py-2">{emp.contacto_emergencia}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TablaEmpleados;
