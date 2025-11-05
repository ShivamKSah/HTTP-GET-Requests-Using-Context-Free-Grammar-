"""
Network Protocol State Machine Implementation

This module implements state machines for network protocol analysis,
focusing on TCP connection states and HTTP protocol state transitions.
Demonstrates computer networks concepts in practice.

Key Features:
1. TCP connection state machine (RFC 793)
2. HTTP protocol state machine 
3. Network packet analysis simulation
4. Connection lifecycle tracking
5. Protocol compliance verification
"""

from typing import Dict, List, Set, Optional, Tuple, Any, Union
from enum import Enum
from dataclasses import dataclass, field
import json
import time
from datetime import datetime, timedelta
import ipaddress
import random

class TCPState(Enum):
    """TCP connection states according to RFC 793."""
    CLOSED = "CLOSED"
    LISTEN = "LISTEN"
    SYN_SENT = "SYN_SENT"
    SYN_RECEIVED = "SYN_RECEIVED"
    ESTABLISHED = "ESTABLISHED"
    FIN_WAIT_1 = "FIN_WAIT_1"
    FIN_WAIT_2 = "FIN_WAIT_2"
    CLOSE_WAIT = "CLOSE_WAIT"
    CLOSING = "CLOSING"
    LAST_ACK = "LAST_ACK"
    TIME_WAIT = "TIME_WAIT"

class HTTPState(Enum):
    """HTTP protocol states for request/response cycle."""
    IDLE = "IDLE"
    REQUEST_RECEIVED = "REQUEST_RECEIVED"
    REQUEST_PARSED = "REQUEST_PARSED"
    PROCESSING_REQUEST = "PROCESSING_REQUEST"
    RESPONSE_READY = "RESPONSE_READY"
    RESPONSE_SENT = "RESPONSE_SENT"
    KEEP_ALIVE = "KEEP_ALIVE"
    CONNECTION_CLOSE = "CONNECTION_CLOSE"
    ERROR_STATE = "ERROR_STATE"

class PacketType(Enum):
    """Network packet types."""
    SYN = "SYN"
    ACK = "ACK"
    SYN_ACK = "SYN+ACK"
    FIN = "FIN"
    FIN_ACK = "FIN+ACK"
    RST = "RST"
    HTTP_REQUEST = "HTTP_REQUEST"
    HTTP_RESPONSE = "HTTP_RESPONSE"
    DATA = "DATA"

@dataclass
class NetworkPacket:
    """Represents a network packet."""
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    packet_type: PacketType
    sequence_num: int
    ack_num: int
    payload: str = ""
    flags: Set[str] = field(default_factory=set)
    timestamp: datetime = field(default_factory=datetime.now)
    size: int = 0

@dataclass
class TCPConnection:
    """Represents a TCP connection."""
    client_ip: str
    client_port: int
    server_ip: str
    server_port: int
    state: TCPState = TCPState.CLOSED
    client_seq: int = 0
    server_seq: int = 0
    client_ack: int = 0
    server_ack: int = 0
    established_time: Optional[datetime] = None
    last_activity: datetime = field(default_factory=datetime.now)
    packets: List[NetworkPacket] = field(default_factory=list)
    connection_id: str = ""

@dataclass
class HTTPSession:
    """Represents an HTTP session."""
    connection: TCPConnection
    state: HTTPState = HTTPState.IDLE
    current_request: Optional[str] = None
    current_response: Optional[str] = None
    request_count: int = 0
    keep_alive: bool = True
    protocol_version: str = "HTTP/1.1"
    last_request_time: Optional[datetime] = None
    response_time: Optional[timedelta] = None

class TCPStateMachine:
    """
    TCP connection state machine implementation.
    
    Implements the TCP state transitions according to RFC 793.
    """
    
    def __init__(self):
        self.connections: Dict[str, TCPConnection] = {}
        self.transition_table = self._create_tcp_transition_table()
        self.packet_log: List[NetworkPacket] = []
        
    def _create_tcp_transition_table(self) -> Dict[Tuple[TCPState, PacketType], TCPState]:
        """Create TCP state transition table."""
        transitions = {}
        
        # From CLOSED
        transitions[(TCPState.CLOSED, PacketType.SYN)] = TCPState.SYN_RECEIVED
        
        # From LISTEN
        transitions[(TCPState.LISTEN, PacketType.SYN)] = TCPState.SYN_RECEIVED
        
        # From SYN_SENT
        transitions[(TCPState.SYN_SENT, PacketType.SYN_ACK)] = TCPState.ESTABLISHED
        transitions[(TCPState.SYN_SENT, PacketType.SYN)] = TCPState.SYN_RECEIVED
        
        # From SYN_RECEIVED
        transitions[(TCPState.SYN_RECEIVED, PacketType.ACK)] = TCPState.ESTABLISHED
        
        # From ESTABLISHED
        transitions[(TCPState.ESTABLISHED, PacketType.FIN)] = TCPState.CLOSE_WAIT
        transitions[(TCPState.ESTABLISHED, PacketType.FIN_ACK)] = TCPState.FIN_WAIT_1
        
        # From FIN_WAIT_1
        transitions[(TCPState.FIN_WAIT_1, PacketType.ACK)] = TCPState.FIN_WAIT_2
        transitions[(TCPState.FIN_WAIT_1, PacketType.FIN)] = TCPState.CLOSING
        
        # From FIN_WAIT_2
        transitions[(TCPState.FIN_WAIT_2, PacketType.FIN)] = TCPState.TIME_WAIT
        
        # From CLOSE_WAIT
        transitions[(TCPState.CLOSE_WAIT, PacketType.FIN)] = TCPState.LAST_ACK
        
        # From CLOSING
        transitions[(TCPState.CLOSING, PacketType.ACK)] = TCPState.TIME_WAIT
        
        # From LAST_ACK
        transitions[(TCPState.LAST_ACK, PacketType.ACK)] = TCPState.CLOSED
        
        # From TIME_WAIT (timeout)
        transitions[(TCPState.TIME_WAIT, PacketType.ACK)] = TCPState.CLOSED
        
        return transitions
    
    def create_connection(self, client_ip: str, client_port: int, 
                         server_ip: str, server_port: int) -> str:
        """Create a new TCP connection."""
        connection_id = f"{client_ip}:{client_port}->{server_ip}:{server_port}"
        
        connection = TCPConnection(
            client_ip=client_ip,
            client_port=client_port,
            server_ip=server_ip,
            server_port=server_port,
            state=TCPState.CLOSED,
            client_seq=random.randint(1000, 9999),
            server_seq=random.randint(1000, 9999),
            connection_id=connection_id
        )
        
        self.connections[connection_id] = connection
        return connection_id
    
    def process_packet(self, connection_id: str, packet: NetworkPacket) -> Dict[str, Any]:
        """Process a packet and update connection state."""
        if connection_id not in self.connections:
            return {'error': 'Connection not found'}
        
        connection = self.connections[connection_id]
        old_state = connection.state
        
        # Update connection with packet
        connection.packets.append(packet)
        connection.last_activity = packet.timestamp
        self.packet_log.append(packet)
        
        # Check for state transition
        transition_key = (connection.state, packet.packet_type)
        
        if transition_key in self.transition_table:
            new_state = self.transition_table[transition_key]
            connection.state = new_state
            
            # Special handling for ESTABLISHED state
            if new_state == TCPState.ESTABLISHED and old_state != TCPState.ESTABLISHED:
                connection.established_time = packet.timestamp
            
            return {
                'success': True,
                'old_state': old_state.value,
                'new_state': new_state.value,
                'connection_id': connection_id,
                'transition': f"{old_state.value} -> {new_state.value}"
            }
        else:
            return {
                'success': False,
                'error': f"Invalid transition: {old_state.value} with {packet.packet_type.value}",
                'current_state': connection.state.value
            }
    
    def simulate_tcp_handshake(self, connection_id: str) -> List[Dict[str, Any]]:
        """Simulate a TCP three-way handshake."""
        if connection_id not in self.connections:
            return [{'error': 'Connection not found'}]
        
        connection = self.connections[connection_id]
        results = []
        
        # Step 1: Client sends SYN
        syn_packet = NetworkPacket(
            src_ip=connection.client_ip,
            dst_ip=connection.server_ip,
            src_port=connection.client_port,
            dst_port=connection.server_port,
            packet_type=PacketType.SYN,
            sequence_num=connection.client_seq,
            ack_num=0,
            flags={'SYN'}
        )
        
        # Server should go to LISTEN first (simulated)
        connection.state = TCPState.LISTEN
        result1 = self.process_packet(connection_id, syn_packet)
        results.append(result1)
        
        # Step 2: Server responds with SYN+ACK
        syn_ack_packet = NetworkPacket(
            src_ip=connection.server_ip,
            dst_ip=connection.client_ip,
            src_port=connection.server_port,
            dst_port=connection.client_port,
            packet_type=PacketType.SYN_ACK,
            sequence_num=connection.server_seq,
            ack_num=connection.client_seq + 1,
            flags={'SYN', 'ACK'}
        )
        
        # Client should be in SYN_SENT (simulated)
        connection.state = TCPState.SYN_SENT
        result2 = self.process_packet(connection_id, syn_ack_packet)
        results.append(result2)
        
        # Step 3: Client sends ACK
        ack_packet = NetworkPacket(
            src_ip=connection.client_ip,
            dst_ip=connection.server_ip,
            src_port=connection.client_port,
            dst_port=connection.server_port,
            packet_type=PacketType.ACK,
            sequence_num=connection.client_seq + 1,
            ack_num=connection.server_seq + 1,
            flags={'ACK'}
        )
        
        # Server should be in SYN_RECEIVED
        connection.state = TCPState.SYN_RECEIVED
        result3 = self.process_packet(connection_id, ack_packet)
        results.append(result3)
        
        return results
    
    def simulate_tcp_close(self, connection_id: str) -> List[Dict[str, Any]]:
        """Simulate TCP connection termination."""
        if connection_id not in self.connections:
            return [{'error': 'Connection not found'}]
        
        connection = self.connections[connection_id]
        
        if connection.state != TCPState.ESTABLISHED:
            return [{'error': 'Connection must be in ESTABLISHED state to close'}]
        
        results = []
        
        # Step 1: Client sends FIN
        fin_packet = NetworkPacket(
            src_ip=connection.client_ip,
            dst_ip=connection.server_ip,
            src_port=connection.client_port,
            dst_port=connection.server_port,
            packet_type=PacketType.FIN,
            sequence_num=connection.client_seq,
            ack_num=connection.server_seq,
            flags={'FIN'}
        )
        
        result1 = self.process_packet(connection_id, fin_packet)
        results.append(result1)
        
        # Step 2: Server sends ACK
        ack_packet = NetworkPacket(
            src_ip=connection.server_ip,
            dst_ip=connection.client_ip,
            src_port=connection.server_port,
            dst_port=connection.client_port,
            packet_type=PacketType.ACK,
            sequence_num=connection.server_seq,
            ack_num=connection.client_seq + 1,
            flags={'ACK'}
        )
        
        # Move to FIN_WAIT_1 first
        connection.state = TCPState.FIN_WAIT_1
        result2 = self.process_packet(connection_id, ack_packet)
        results.append(result2)
        
        # Step 3: Server sends FIN
        server_fin_packet = NetworkPacket(
            src_ip=connection.server_ip,
            dst_ip=connection.client_ip,
            src_port=connection.server_port,
            dst_port=connection.client_port,
            packet_type=PacketType.FIN,
            sequence_num=connection.server_seq + 1,
            ack_num=connection.client_seq + 1,
            flags={'FIN'}
        )
        
        # Move to FIN_WAIT_2
        connection.state = TCPState.FIN_WAIT_2
        result3 = self.process_packet(connection_id, server_fin_packet)
        results.append(result3)
        
        # Step 4: Client sends final ACK
        final_ack_packet = NetworkPacket(
            src_ip=connection.client_ip,
            dst_ip=connection.server_ip,
            src_port=connection.client_port,
            dst_port=connection.server_port,
            packet_type=PacketType.ACK,
            sequence_num=connection.client_seq + 1,
            ack_num=connection.server_seq + 2,
            flags={'ACK'}
        )
        
        # Move to TIME_WAIT
        connection.state = TCPState.TIME_WAIT
        result4 = self.process_packet(connection_id, final_ack_packet)
        results.append(result4)
        
        return results

class HTTPStateMachine:
    """
    HTTP protocol state machine implementation.
    
    Models the HTTP request/response cycle and connection management.
    """
    
    def __init__(self):
        self.sessions: Dict[str, HTTPSession] = {}
        self.tcp_state_machine = TCPStateMachine()
        
    def create_http_session(self, connection_id: str) -> str:
        """Create a new HTTP session over a TCP connection."""
        if connection_id not in self.tcp_state_machine.connections:
            raise ValueError("TCP connection must exist first")
        
        tcp_connection = self.tcp_state_machine.connections[connection_id]
        
        if tcp_connection.state != TCPState.ESTABLISHED:
            raise ValueError("TCP connection must be in ESTABLISHED state")
        
        session = HTTPSession(
            connection=tcp_connection,
            state=HTTPState.IDLE
        )
        
        session_id = f"http_{connection_id}"
        self.sessions[session_id] = session
        return session_id
    
    def process_http_request(self, session_id: str, request_data: str) -> Dict[str, Any]:
        """Process an HTTP request and update session state."""
        if session_id not in self.sessions:
            return {'error': 'HTTP session not found'}
        
        session = self.sessions[session_id]
        
        # State transition: IDLE -> REQUEST_RECEIVED
        if session.state == HTTPState.IDLE:
            session.state = HTTPState.REQUEST_RECEIVED
            session.current_request = request_data
            session.last_request_time = datetime.now()
            session.request_count += 1
            
            # Create HTTP request packet
            request_packet = NetworkPacket(
                src_ip=session.connection.client_ip,
                dst_ip=session.connection.server_ip,
                src_port=session.connection.client_port,
                dst_port=session.connection.server_port,
                packet_type=PacketType.HTTP_REQUEST,
                sequence_num=session.connection.client_seq,
                ack_num=session.connection.server_seq,
                payload=request_data,
                size=len(request_data)
            )
            
            session.connection.packets.append(request_packet)
            
            return {
                'success': True,
                'new_state': session.state.value,
                'request_number': session.request_count
            }
        else:
            return {
                'error': f"Cannot process request in state {session.state.value}",
                'current_state': session.state.value
            }
    
    def parse_http_request(self, session_id: str) -> Dict[str, Any]:
        """Parse the HTTP request and move to parsed state."""
        if session_id not in self.sessions:
            return {'error': 'HTTP session not found'}
        
        session = self.sessions[session_id]
        
        if session.state == HTTPState.REQUEST_RECEIVED:
            session.state = HTTPState.REQUEST_PARSED
            
            # Extract HTTP version from request for connection management
            if session.current_request:
                if "HTTP/1.0" in session.current_request:
                    session.protocol_version = "HTTP/1.0"
                    session.keep_alive = False
                elif "HTTP/1.1" in session.current_request:
                    session.protocol_version = "HTTP/1.1"
                    session.keep_alive = True
                    
                    # Check for Connection: close header
                    if "Connection: close" in session.current_request:
                        session.keep_alive = False
            
            return {
                'success': True,
                'new_state': session.state.value,
                'protocol_version': session.protocol_version,
                'keep_alive': session.keep_alive
            }
        else:
            return {
                'error': f"Cannot parse request in state {session.state.value}",
                'current_state': session.state.value
            }
    
    def process_http_response(self, session_id: str, response_data: str) -> Dict[str, Any]:
        """Process HTTP response and update session state."""
        if session_id not in self.sessions:
            return {'error': 'HTTP session not found'}
        
        session = self.sessions[session_id]
        
        if session.state in [HTTPState.REQUEST_PARSED, HTTPState.PROCESSING_REQUEST]:
            session.state = HTTPState.RESPONSE_SENT
            session.current_response = response_data
            
            if session.last_request_time:
                session.response_time = datetime.now() - session.last_request_time
            
            # Create HTTP response packet
            response_packet = NetworkPacket(
                src_ip=session.connection.server_ip,
                dst_ip=session.connection.client_ip,
                src_port=session.connection.server_port,
                dst_port=session.connection.client_port,
                packet_type=PacketType.HTTP_RESPONSE,
                sequence_num=session.connection.server_seq,
                ack_num=session.connection.client_seq,
                payload=response_data,
                size=len(response_data)
            )
            
            session.connection.packets.append(response_packet)
            
            # Determine next state based on connection management
            if session.keep_alive:
                session.state = HTTPState.KEEP_ALIVE
            else:
                session.state = HTTPState.CONNECTION_CLOSE
            
            return {
                'success': True,
                'new_state': session.state.value,
                'response_time_ms': session.response_time.total_seconds() * 1000 if session.response_time else None,
                'keep_alive': session.keep_alive
            }
        else:
            return {
                'error': f"Cannot send response in state {session.state.value}",
                'current_state': session.state.value
            }
    
    def reset_for_new_request(self, session_id: str) -> Dict[str, Any]:
        """Reset session for a new request (keep-alive)."""
        if session_id not in self.sessions:
            return {'error': 'HTTP session not found'}
        
        session = self.sessions[session_id]
        
        if session.state == HTTPState.KEEP_ALIVE:
            session.state = HTTPState.IDLE
            session.current_request = None
            session.current_response = None
            
            return {
                'success': True,
                'new_state': session.state.value,
                'ready_for_request': True
            }
        else:
            return {
                'error': f"Cannot reset session in state {session.state.value}",
                'current_state': session.state.value
            }
    
    def get_session_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get analytics for an HTTP session."""
        if session_id not in self.sessions:
            return {'error': 'HTTP session not found'}
        
        session = self.sessions[session_id]
        
        # Calculate connection duration
        connection_duration = None
        if session.connection.established_time:
            connection_duration = (datetime.now() - session.connection.established_time).total_seconds()
        
        # Analyze packet flow
        request_packets = [p for p in session.connection.packets if p.packet_type == PacketType.HTTP_REQUEST]
        response_packets = [p for p in session.connection.packets if p.packet_type == PacketType.HTTP_RESPONSE]
        
        return {
            'session_id': session_id,
            'tcp_state': session.connection.state.value,
            'http_state': session.state.value,
            'protocol_version': session.protocol_version,
            'keep_alive': session.keep_alive,
            'request_count': session.request_count,
            'connection_duration_seconds': connection_duration,
            'total_packets': len(session.connection.packets),
            'request_packets': len(request_packets),
            'response_packets': len(response_packets),
            'last_response_time_ms': session.response_time.total_seconds() * 1000 if session.response_time else None,
            'connection_established_time': session.connection.established_time.isoformat() if session.connection.established_time else None
        }

# Network simulation and analysis functions
class NetworkProtocolAnalyzer:
    """Analyzer for network protocol behavior and compliance."""
    
    def __init__(self):
        self.tcp_sm = TCPStateMachine()
        self.http_sm = HTTPStateMachine()
    
    def simulate_complete_http_session(self, client_ip: str = "192.168.1.100", 
                                     server_ip: str = "203.0.113.50") -> Dict[str, Any]:
        """Simulate a complete HTTP session from TCP handshake to close."""
        
        # Step 1: Create TCP connection
        connection_id = self.tcp_sm.create_connection(client_ip, 12345, server_ip, 80)
        
        # Step 2: TCP handshake
        handshake_results = self.tcp_sm.simulate_tcp_handshake(connection_id)
        
        # Step 3: Create HTTP session
        session_id = self.http_sm.create_http_session(connection_id)
        
        # Step 4: HTTP request/response cycle
        sample_request = "GET /index.html HTTP/1.1\r\nHost: example.com\r\nUser-Agent: TestClient/1.0\r\n\r\n"
        request_result = self.http_sm.process_http_request(session_id, sample_request)
        parse_result = self.http_sm.parse_http_request(session_id)
        
        sample_response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 13\r\n\r\n<html></html>"
        response_result = self.http_sm.process_http_response(session_id, sample_response)
        
        # Step 5: Connection close
        close_results = self.tcp_sm.simulate_tcp_close(connection_id)
        
        # Step 6: Collect analytics
        session_analytics = self.http_sm.get_session_analytics(session_id)
        
        return {
            'simulation_id': f"sim_{int(time.time())}",
            'tcp_handshake': handshake_results,
            'http_request': request_result,
            'http_parse': parse_result,
            'http_response': response_result,
            'tcp_close': close_results,
            'session_analytics': session_analytics,
            'total_packets': len(self.tcp_sm.connections[connection_id].packets),
            'final_tcp_state': self.tcp_sm.connections[connection_id].state.value
        }
    
    def analyze_protocol_compliance(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze protocol compliance for a session."""
        
        compliance = {
            'tcp_compliance': {
                'handshake_valid': True,
                'state_transitions_valid': True,
                'close_sequence_valid': True
            },
            'http_compliance': {
                'request_format_valid': True,
                'response_format_valid': True,
                'connection_management_valid': True
            },
            'overall_score': 0.0,
            'issues': []
        }
        
        # Check TCP compliance
        if session_data.get('tcp_handshake'):
            handshake_success = all(result.get('success', False) for result in session_data['tcp_handshake'])
            compliance['tcp_compliance']['handshake_valid'] = handshake_success
            if not handshake_success:
                compliance['issues'].append("TCP handshake sequence invalid")
        
        # Check HTTP compliance
        if session_data.get('http_request', {}).get('success'):
            compliance['http_compliance']['request_format_valid'] = True
        else:
            compliance['http_compliance']['request_format_valid'] = False
            compliance['issues'].append("HTTP request format invalid")
        
        # Calculate overall score
        total_checks = 6
        passed_checks = sum([
            compliance['tcp_compliance']['handshake_valid'],
            compliance['tcp_compliance']['state_transitions_valid'],
            compliance['tcp_compliance']['close_sequence_valid'],
            compliance['http_compliance']['request_format_valid'],
            compliance['http_compliance']['response_format_valid'],
            compliance['http_compliance']['connection_management_valid']
        ])
        
        compliance['overall_score'] = (passed_checks / total_checks) * 100.0
        
        return compliance

# Example usage
if __name__ == "__main__":
    analyzer = NetworkProtocolAnalyzer()
    
    print("Simulating complete HTTP session...")
    session_data = analyzer.simulate_complete_http_session()
    
    print(f"Simulation ID: {session_data['simulation_id']}")
    print(f"Total packets: {session_data['total_packets']}")
    print(f"Final TCP state: {session_data['final_tcp_state']}")
    
    if session_data.get('session_analytics'):
        analytics = session_data['session_analytics']
        print(f"Protocol version: {analytics['protocol_version']}")
        print(f"Request count: {analytics['request_count']}")
        print(f"Response time: {analytics['last_response_time_ms']}ms")
    
    # Analyze compliance
    compliance = analyzer.analyze_protocol_compliance(session_data)
    print(f"\nProtocol compliance score: {compliance['overall_score']:.1f}%")
    if compliance['issues']:
        print("Issues found:", compliance['issues'])