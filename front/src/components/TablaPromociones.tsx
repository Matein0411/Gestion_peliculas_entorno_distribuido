import React from 'react';

interface Promocion {
  promocion_id: number;
  codigo_promo: string;
  descripcion: string;
  descuento_porcentaje: number;
  fecha_creacion: string;
  ciudad: string;
}

interface Props {
  titulo: string;
  promociones: Promocion[];
}

const TablaPromociones: React.FC<Props> = ({ titulo, promociones }) => {
  return (
     <div className="overflow-x-auto mt-6 shadow-lg rounded-lg border border-gray-200 bg-white">
        {/* <h3 className="text-xl font-bold mb-4 text-gray-800">{titulo}</h3> */}
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-blue-100 text-blue-800 font-semibold">
          <tr>
            <th className="px-4 py-2">ID</th>
            <th className="px-4 py-2">Código</th>
            <th className="px-4 py-2">Descripción</th>
            <th className="px-4 py-2">Descuento (%)</th>
            <th className="px-4 py-2">Fecha</th>
            <th className="px-4 py-2">Ciudad</th>
          </tr>
        </thead>
        <tbody>
          {promociones.map((p) => (
            <tr key={p.promocion_id} className="text-center border-b">
              <td className="px-4 py-2">{p.promocion_id}</td>
              <td className="px-4 py-2">{p.codigo_promo}</td>
              <td className="px-4 py-2">{p.descripcion}</td>
              <td className="px-4 py-2">{p.descuento_porcentaje}</td>
              <td className="px-4 py-2">{new Date(p.fecha_creacion).toLocaleDateString()}</td>
              <td className="px-4 py-2">{p.ciudad}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TablaPromociones;
