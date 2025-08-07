import React from 'react';
import { CheckCircle, Database, Clock } from 'lucide-react';

interface Operation {
  id: string;
  type: string;
  description: string;
  status: 'completed' | 'running' | 'pending';
  timestamp: string;
  details?: string;
}

interface ResultsPanelProps {
  operations: Operation[];
  isVisible: boolean;
}

const ResultsPanel: React.FC<ResultsPanelProps> = ({ operations, isVisible }) => {
  if (!isVisible) return null;

  return (
    <div className="mt-8 bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
      <div className="bg-gradient-to-r from-gray-800 to-gray-900 px-6 py-4">
        <div className="flex items-center space-x-3">
          <Database className="h-6 w-6 text-blue-400" />
          <h3 className="text-xl font-bold text-white">Registro de Operaciones</h3>
        </div>
      </div>
      
      <div className="max-h-96 overflow-y-auto">
        {operations.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <Database className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p>No hay operaciones registradas aún.</p>
            <p className="text-sm mt-2">Haz clic en cualquier botón para comenzar.</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-100">
            {operations.map((operation) => (
              <div key={operation.id} className="p-4 hover:bg-gray-50 transition-colors duration-200">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 mt-1">
                    {operation.status === 'completed' && (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    )}
                    {operation.status === 'running' && (
                      <Clock className="h-5 w-5 text-yellow-500 animate-spin" />
                    )}
                    {operation.status === 'pending' && (
                      <Clock className="h-5 w-5 text-gray-400" />
                    )}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="font-semibold text-gray-900">{operation.type}</p>
                        <p className="text-gray-600 text-sm mt-1">{operation.description}</p>
                        {operation.details && (
                          <p className="text-xs text-gray-500 mt-2 bg-gray-100 p-2 rounded font-mono">
                            {operation.details}
                          </p>
                        )}
                      </div>
                      <span className="text-xs text-gray-400 ml-4 flex-shrink-0">
                        {operation.timestamp}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsPanel;