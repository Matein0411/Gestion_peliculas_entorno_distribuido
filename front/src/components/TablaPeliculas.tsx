import React from 'react';

const TablaPeliculas = ({ titulo, peliculas }: { titulo: string, peliculas: any[] }) => {
  return (
    <div className="overflow-x-auto mt-6 shadow-lg rounded-lg border border-gray-200 bg-white">
      <h3 className="text-xl font-bold mb-4 text-gray-800">{titulo}</h3> 
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-blue-100 text-blue-800 font-semibold">
          <tr>
            <th className="px-4 py-2">ID</th>
            <th className="px-4 py-2">Título</th>
            <th className="px-4 py-2">Género</th>
            <th className="px-4 py-2">Director</th>
            <th className="px-4 py-2">Clasificación</th>
            <th className="px-4 py-2">Sinopsis</th>
            <th className="px-4 py-2">Poster</th>
            <th className="px-4 py-2">Fecha</th>
          </tr>
        </thead>
        <tbody>
          {peliculas?.map((peli, index) => (
            <tr key={index} className="text-center border-b">
              <td className="px-4 py-2">{peli.pelicula_id}</td>
              <td className="px-4 py-2">{peli.titulo}</td>
              <td className="px-4 py-2">{peli.genero}</td>
              <td className="px-4 py-2">{peli.director}</td>
              <td className="px-4 py-2">{peli.clasificacion}</td>
              <td className="px-4 py-2">{peli.sinopsis}</td>
              <td className="px-4 py-2">
                <img src={peli.url_poster} alt="Poster" className="h-16 mx-auto" />
              </td>
              <td className="px-4 py-2">{new Date(peli.fecha_creacion).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TablaPeliculas;
