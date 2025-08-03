import React from 'react';
import { Server, Wifi, WifiOff } from 'lucide-react';

interface Node {
  id: string;
  name: string;
  status: 'online' | 'offline' | 'syncing';
  dbms: string;
  records: number;
}

interface NodeStatusProps {
  nodes: Node[];
}

const NodeStatus: React.FC<NodeStatusProps> = ({ nodes }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'text-green-500';
      case 'offline': return 'text-red-500';
      case 'syncing': return 'text-yellow-500';
      default: return 'text-gray-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online': return <Wifi className="h-4 w-4" />;
      case 'offline': return <WifiOff className="h-4 w-4" />;
      case 'syncing': return <Wifi className="h-4 w-4 animate-pulse" />;
      default: return <WifiOff className="h-4 w-4" />;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-8">
      <div className="flex items-center space-x-3 mb-6">
        <Server className="h-6 w-6 text-blue-600" />
        <h3 className="text-xl font-bold text-gray-900">Estado de los Nodos</h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {nodes.map((node) => (
          <div key={node.id} className="bg-gray-50 rounded-lg p-4 border border-gray-200">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <Server className="h-5 w-5 text-gray-600" />
                <span className="font-semibold text-gray-900">{node.name}</span>
              </div>
              <div className={`flex items-center space-x-1 ${getStatusColor(node.status)}`}>
                {getStatusIcon(node.status)}
                <span className="text-sm capitalize">{node.status}</span>
              </div>
            </div>
            
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">DBMS:</span>
                <span className="font-medium">{node.dbms}</span>
              </div>

            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NodeStatus;