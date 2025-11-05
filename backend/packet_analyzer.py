"""
Network Packet Analysis Visualization for HTTP Requests

This module provides packet-level analysis and visualization for HTTP requests
using formal language concepts and network protocol understanding.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

class PacketType(Enum):
    TCP_SYN = "tcp_syn"
    TCP_ACK = "tcp_ack"
    TCP_FIN = "tcp_fin"
    HTTP_REQUEST = "http_request"
    HTTP_RESPONSE = "http_response"

class ProtocolLayer(Enum):
    PHYSICAL = "physical"
    DATA_LINK = "data_link"
    NETWORK = "network"
    TRANSPORT = "transport"
    APPLICATION = "application"

@dataclass
class PacketHeader:
    """Represents a packet header."""
    name: str
    value: str
    layer: ProtocolLayer
    size_bytes: int
    is_valid: bool = True
    errors: Optional[List[str]] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

@dataclass
class NetworkPacket:
    """Represents a network packet."""
    packet_id: str
    packet_type: PacketType
    timestamp: str
    source_ip: str
    dest_ip: str
    source_port: int
    dest_port: int
    headers: List[PacketHeader]
    payload: str
    size_bytes: int
    protocol_stack: List[ProtocolLayer]
    is_valid: bool = True
    errors: Optional[List[str]] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

class HTTPPacketAnalyzer:
    """Analyzes HTTP packets using formal language principles."""
    
    def __init__(self):
        self.http_methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'TRACE']
        self.http_versions = ['HTTP/1.0', 'HTTP/1.1', 'HTTP/2.0']
        self.status_codes = {
            200: 'OK', 201: 'Created', 204: 'No Content',
            301: 'Moved Permanently', 302: 'Found', 304: 'Not Modified',
            400: 'Bad Request', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found',
            500: 'Internal Server Error', 502: 'Bad Gateway', 503: 'Service Unavailable'
        }
        
    def analyze_http_request_packet(self, raw_request: str, 
                                  source_ip: str = "192.168.1.100", 
                                  dest_ip: str = "192.168.1.1") -> NetworkPacket:
        """Analyze an HTTP request and create packet representation."""
        packet_id = f"pkt_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Parse HTTP request
        lines = raw_request.strip().split('\n')
        if not lines:
            return self._create_error_packet(packet_id, "Empty request")
        
        # Parse request line
        request_line = lines[0].strip()
        method, path, version = self._parse_request_line(request_line)
        
        # Parse headers
        headers = []
        payload = ""
        payload_start = -1
        
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "":
                payload_start = i + 1
                break
            
            if ':' in line:
                header_name, header_value = line.split(':', 1)
                header = PacketHeader(
                    name=header_name.strip(),
                    value=header_value.strip(),
                    layer=ProtocolLayer.APPLICATION,
                    size_bytes=len(line.encode('utf-8'))
                )
                headers.append(header)
        
        # Extract payload if present
        if payload_start > 0 and payload_start < len(lines):
            payload = '\n'.join(lines[payload_start:])
        
        # Create protocol stack
        protocol_stack = [
            ProtocolLayer.PHYSICAL,
            ProtocolLayer.DATA_LINK,
            ProtocolLayer.NETWORK,
            ProtocolLayer.TRANSPORT,
            ProtocolLayer.APPLICATION
        ]
        
        # Add TCP and IP headers
        tcp_headers = self._create_tcp_headers(source_ip, dest_ip, 80)
        ip_headers = self._create_ip_headers(source_ip, dest_ip)
        
        all_headers = ip_headers + tcp_headers + headers
        
        # Calculate total size
        total_size = sum(h.size_bytes for h in all_headers) + len(payload.encode('utf-8'))
        
        packet = NetworkPacket(
            packet_id=packet_id,
            packet_type=PacketType.HTTP_REQUEST,
            timestamp=datetime.now().isoformat(),
            source_ip=source_ip,
            dest_ip=dest_ip,
            source_port=12345,  # Simulated client port
            dest_port=80,       # HTTP port
            headers=all_headers,
            payload=payload,
            size_bytes=total_size,
            protocol_stack=protocol_stack
        )
        
        # Validate packet
        self._validate_packet(packet, method, path, version)
        
        return packet
    
    def _parse_request_line(self, request_line: str) -> Tuple[str, str, str]:
        """Parse HTTP request line."""
        parts = request_line.split(' ')
        if len(parts) != 3:
            raise ValueError(f"Invalid request line format: {request_line}")
        return parts[0], parts[1], parts[2]
    
    def _create_tcp_headers(self, source_ip: str, dest_ip: str, dest_port: int) -> List[PacketHeader]:
        """Create simulated TCP headers."""
        return [
            PacketHeader("TCP-Source-Port", "12345", ProtocolLayer.TRANSPORT, 2),
            PacketHeader("TCP-Dest-Port", str(dest_port), ProtocolLayer.TRANSPORT, 2),
            PacketHeader("TCP-Sequence", "1000000", ProtocolLayer.TRANSPORT, 4),
            PacketHeader("TCP-Acknowledgment", "0", ProtocolLayer.TRANSPORT, 4),
            PacketHeader("TCP-Flags", "PSH,ACK", ProtocolLayer.TRANSPORT, 2),
            PacketHeader("TCP-Window", "65535", ProtocolLayer.TRANSPORT, 2),
            PacketHeader("TCP-Checksum", "0x1234", ProtocolLayer.TRANSPORT, 2),
        ]
    
    def _create_ip_headers(self, source_ip: str, dest_ip: str) -> List[PacketHeader]:
        """Create simulated IP headers."""
        return [
            PacketHeader("IP-Version", "4", ProtocolLayer.NETWORK, 1),
            PacketHeader("IP-Header-Length", "20", ProtocolLayer.NETWORK, 1),
            PacketHeader("IP-Type-of-Service", "0", ProtocolLayer.NETWORK, 1),
            PacketHeader("IP-Total-Length", "1500", ProtocolLayer.NETWORK, 2),
            PacketHeader("IP-Identification", "12345", ProtocolLayer.NETWORK, 2),
            PacketHeader("IP-Flags", "010", ProtocolLayer.NETWORK, 2),
            PacketHeader("IP-TTL", "64", ProtocolLayer.NETWORK, 1),
            PacketHeader("IP-Protocol", "6", ProtocolLayer.NETWORK, 1),
            PacketHeader("IP-Header-Checksum", "0xABCD", ProtocolLayer.NETWORK, 2),
            PacketHeader("IP-Source", source_ip, ProtocolLayer.NETWORK, 4),
            PacketHeader("IP-Destination", dest_ip, ProtocolLayer.NETWORK, 4),
        ]
    
    def _validate_packet(self, packet: NetworkPacket, method: str, path: str, version: str):
        """Validate packet using formal rules."""
        errors = []
        
        # Validate HTTP method
        if method not in self.http_methods:
            errors.append(f"Invalid HTTP method: {method}")
        
        # Validate HTTP version
        if version not in self.http_versions:
            errors.append(f"Invalid HTTP version: {version}")
        
        # Validate path format
        if not path.startswith('/'):
            errors.append(f"Invalid path format: {path}")
        
        # Validate required headers for specific methods
        header_names = [h.name.lower() for h in packet.headers if h.layer == ProtocolLayer.APPLICATION]
        
        if method in ['POST', 'PUT', 'PATCH']:
            if 'content-length' not in header_names and 'transfer-encoding' not in header_names:
                errors.append("Missing Content-Length or Transfer-Encoding header for request with body")
        
        if 'host' not in header_names:
            errors.append("Missing required Host header")
        
        if packet.errors is None:
            packet.errors = []
        packet.errors.extend(errors)
        packet.is_valid = len(errors) == 0
    
    def _create_error_packet(self, packet_id: str, error_msg: str) -> NetworkPacket:
        """Create an error packet."""
        return NetworkPacket(
            packet_id=packet_id,
            packet_type=PacketType.HTTP_REQUEST,
            timestamp=datetime.now().isoformat(),
            source_ip="0.0.0.0",
            dest_ip="0.0.0.0",
            source_port=0,
            dest_port=0,
            headers=[],
            payload="",
            size_bytes=0,
            protocol_stack=[],
            is_valid=False,
            errors=[error_msg]
        )
    
    def generate_packet_visualization_data(self, packet: NetworkPacket) -> Dict[str, Any]:
        """Generate data for packet visualization."""
        layers_data = {}
        
        for layer in ProtocolLayer:
            layer_headers = [h for h in packet.headers if h.layer == layer]
            if layer_headers:
                layers_data[layer.value] = {
                    'headers': [
                        {
                            'name': h.name,
                            'value': h.value,
                            'size': h.size_bytes,
                            'valid': h.is_valid,
                            'errors': h.errors
                        } for h in layer_headers
                    ],
                    'total_size': sum(h.size_bytes for h in layer_headers),
                    'header_count': len(layer_headers)
                }
        
        return {
            'packet_info': {
                'id': packet.packet_id,
                'type': packet.packet_type.value,
                'timestamp': packet.timestamp,
                'source': f"{packet.source_ip}:{packet.source_port}",
                'destination': f"{packet.dest_ip}:{packet.dest_port}",
                'total_size': packet.size_bytes,
                'is_valid': packet.is_valid,
                'errors': packet.errors
            },
            'protocol_layers': layers_data,
            'payload_info': {
                'size': len(packet.payload.encode('utf-8')),
                'preview': packet.payload[:100] + "..." if len(packet.payload) > 100 else packet.payload,
                'content_type': 'text/plain'
            },
            'flow_diagram': self._generate_flow_diagram(packet),
            'statistics': {
                'header_distribution': {
                    layer.value: len([h for h in packet.headers if h.layer == layer])
                    for layer in ProtocolLayer
                },
                'size_distribution': {
                    layer.value: sum(h.size_bytes for h in packet.headers if h.layer == layer)
                    for layer in ProtocolLayer
                }
            }
        }
    
    def _generate_flow_diagram(self, packet: NetworkPacket) -> List[Dict[str, Any]]:
        """Generate flow diagram data for packet journey."""
        flow_steps = []
        
        # Application layer
        flow_steps.append({
            'step': 1,
            'layer': 'Application',
            'description': f'HTTP {packet.packet_type.value.replace("_", " ").title()} created',
            'details': f'Method/Status parsed, headers added',
            'size_added': sum(h.size_bytes for h in packet.headers if h.layer == ProtocolLayer.APPLICATION)
        })
        
        # Transport layer
        flow_steps.append({
            'step': 2,
            'layer': 'Transport',
            'description': 'TCP segment encapsulation',
            'details': f'Source port: {packet.source_port}, Dest port: {packet.dest_port}',
            'size_added': sum(h.size_bytes for h in packet.headers if h.layer == ProtocolLayer.TRANSPORT)
        })
        
        # Network layer
        flow_steps.append({
            'step': 3,
            'layer': 'Network',
            'description': 'IP packet encapsulation',
            'details': f'Source: {packet.source_ip}, Destination: {packet.dest_ip}',
            'size_added': sum(h.size_bytes for h in packet.headers if h.layer == ProtocolLayer.NETWORK)
        })
        
        # Data link layer
        flow_steps.append({
            'step': 4,
            'layer': 'Data Link',
            'description': 'Frame encapsulation',
            'details': 'Ethernet header and trailer added',
            'size_added': 18  # Typical Ethernet frame overhead
        })
        
        # Physical layer
        flow_steps.append({
            'step': 5,
            'layer': 'Physical',
            'description': 'Transmission over medium',
            'details': 'Bits transmitted over network medium',
            'size_added': 0
        })
        
        return flow_steps
    
    def analyze_packet_sequence(self, packets: List[str]) -> Dict[str, Any]:
        """Analyze a sequence of HTTP packets."""
        analyzed_packets = []
        sequence_errors = []
        
        for i, packet_data in enumerate(packets):
            try:
                packet = self.analyze_http_request_packet(packet_data)
                analyzed_packets.append(packet)
            except Exception as e:
                sequence_errors.append(f"Packet {i+1}: {str(e)}")
        
        return {
            'packets': [self.generate_packet_visualization_data(p) for p in analyzed_packets],
            'sequence_analysis': {
                'total_packets': len(packets),
                'valid_packets': len([p for p in analyzed_packets if p.is_valid]),
                'invalid_packets': len([p for p in analyzed_packets if not p.is_valid]),
                'total_size': sum(p.size_bytes for p in analyzed_packets),
                'sequence_errors': sequence_errors
            },
            'flow_analysis': self._analyze_packet_flow(analyzed_packets)
        }
    
    def _analyze_packet_flow(self, packets: List[NetworkPacket]) -> Dict[str, Any]:
        """Analyze the flow between packets."""
        if not packets:
            return {}
        
        flow_data = {
            'connection_info': {
                'source_endpoints': list(set(f"{p.source_ip}:{p.source_port}" for p in packets)),
                'dest_endpoints': list(set(f"{p.dest_ip}:{p.dest_port}" for p in packets)),
                'protocols_used': list(set(p.packet_type.value for p in packets))
            },
            'temporal_analysis': {
                'first_packet': packets[0].timestamp if packets else None,
                'last_packet': packets[-1].timestamp if packets else None,
                'packet_intervals': []
            },
            'size_analysis': {
                'min_size': min(p.size_bytes for p in packets) if packets else 0,
                'max_size': max(p.size_bytes for p in packets) if packets else 0,
                'avg_size': sum(p.size_bytes for p in packets) / len(packets) if packets else 0
            }
        }
        
        return flow_data

# Example usage
if __name__ == "__main__":
    analyzer = HTTPPacketAnalyzer()
    
    sample_request = """GET /api/users HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: application/json
Authorization: Bearer token123"""
    
    packet = analyzer.analyze_http_request_packet(sample_request)
    visualization_data = analyzer.generate_packet_visualization_data(packet)
    
    print(f"Packet ID: {packet.packet_id}")
    print(f"Valid: {packet.is_valid}")
    print(f"Total size: {packet.size_bytes} bytes")
    print(f"Protocol layers: {len(packet.protocol_stack)}")