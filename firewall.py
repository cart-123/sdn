from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import *
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ipv4

class FW(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def s(self, e):
        d, p, o = e.msg.datapath, e.msg.datapath.ofproto_parser, e.msg.datapath.ofproto
        a = [p.OFPActionOutput(o.OFPP_CONTROLLER, o.OFPCML_NO_BUFFER)]
        d.send_msg(p.OFPFlowMod(datapath=d, priority=0, match=p.OFPMatch(), instructions=[p.OFPInstructionActions(o.OFPIT_APPLY_ACTIONS, a)]))

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def p(self, e):
        m, d = e.msg, e.msg.datapath
        p, o = d.ofproto_parser, d.ofproto
        pkt = packet.Packet(m.data)
        ip = pkt.get_protocol(ipv4.ipv4)

        if ip and ip.src == "10.0.0.1" and ip.dst == "10.0.0.3":
            print("blocked")
            d.send_msg(p.OFPFlowMod(datapath=d, priority=1, match=p.OFPMatch(eth_type=0x0800, ipv4_src=ip.src, ipv4_dst=ip.dst), instructions=[]))
            return

        a = [p.OFPActionOutput(o.OFPP_FLOOD)]
        d.send_msg(p.OFPPacketOut(datapath=d, buffer_id=m.buffer_id, in_port=m.match['in_port'], actions=a, data=m.data if m.buffer_id == o.OFP_NO_BUFFER else None))
