#define ETHERTYPE_IPV4 0x0800
#define IPV4_UDP       0x11
#define UDP_GTP_PORT 2152

header_type ethernet_t {
    fields {
        dstAddr : 48;
        srcAddr : 48;
        etherType : 16;
    }
}

header_type ipv4_t {
    fields {
        version : 4;
        ihl : 4;
        diffserv : 8;
        totalLen : 16;
        identification : 16;
        flags : 3;
        fragOffset : 13;
        ttl : 8;
        protocol : 8;
        hdrChecksum : 16;
        srcAddr : 32;
        dstAddr: 32;
    }
}

header_type udp_t {
    fields {
        srcPort : 16;
        dstPort : 16;
        length_ : 16;
        checksum : 16;
    }
}
header_type gtp_t {
    fields {
        version         :3;
        ptFlag          :1; //protocol type - 1 when GTP and 0 when GTP'
        spare           :1; //shall be set to 0
        extHdrFlag      :1;
        seqNumberFlag   :1;
        npduFlag        :1;
        msgType         :8;
        len             :16;
        tunnelEndID     :32;
    }
}

header gtp_t gtp;
header ethernet_t ethernet;
header ipv4_t ipv4;
header udp_t udp;
header udp_t udp_gtp;
header ipv4_t ipv4_gtp;
header ethernet_t ethernet_gtp;

/** PARSERS **/

parser start {
    return parse_ethernet;
}

parser parse_ethernet {
    extract(ethernet);
    return select(latest.etherType) {
        ETHERTYPE_IPV4 : parse_ipv4;
        default: ingress;
    }
}

parser parse_ipv4 {
    extract(ipv4);
    return select(latest.protocol) {
        IPV4_UDP : parse_udp;
        default: ingress;
    }
}


parser parse_udp {
    extract(udp);
            return select(latest.dstPort) {
            UDP_GTP_PORT:  parse_gtp;
            default:            ingress;
        }
}
parser parse_gtp {
//Can i just use "=" to say that other header should take all the data of another?
	ipv4_gtp=ipv4;
	udp_gtp=udp;
	ethernet_gtp=ethernet;
    extract(gtp);
	
    return parse_ethernet;
}

action _drop() {
    drop();
}

action push_gtp(tunelId, dstAddr) {
//Is adding four headers in one function is legal?
	add_header(gtp);
	modify_field(gtp.tunnelEndID, tunelId);
	add_header(udp_gtp);
	modify_field(udp_gtp.srcPort, UDP_GTP_PORT);
	modify_field(udp_gtp.dstPort, UDP_GTP_PORT);
	add_header(ipv4_gtp);
	modify_field(ipv4_gtp.dstAddr, dstAddr);
	add_header(ethernet_gtp);
	modify_field(ethernet_gtp.etherType, ETHERTYPE_IPV4);
}

action pop_gtp(){
	remove_header(ethernet_gtp);
	remove_header(ipv4_gtp);
	remove_header(udp_gtp);
	remove_header(gtp);
}

table fec_table {

    reads {
        ipv4.dstAddr : lpm;
    }

    actions {
        push_gtp;
        _drop;
    }

    size: 1024;
}


table gtp_table {

    reads {
		gtp.tunnelEndID: exact;
		ipv4.dstAddr: exact;
    }

    actions {
        pop_gtp;
        _drop;
    }

    size: 1024;
}
action forward(intf) {
    modify_field(standard_metadata.egress_spec, intf);
}


table gtplookup_table {

    reads {
        gtp.tunnelEndID : exact;
    }

    actions {
        forward;
        _drop;
    }

    size: 1024;

}

table iplookup_table {

    reads {
        ipv4.dstAddr : exact;
    }

    actions {
        forward;
        _drop;
    }

    size: 1024;

}

action rewrite_macs(srcMac, dstMac) {
    modify_field(ethernet.srcAddr, srcMac);
    modify_field(ethernet.dstAddr, dstMac);
}

table switching_table {

    reads {
        standard_metadata.egress_spec : exact;
    }

    actions {
        rewrite_macs;
        _drop;
    }

    size: 1024;

}

control ingress {
    apply(fec_table);
    apply(gtp_table);
    apply(gtplookup_table);
    if (standard_metadata.egress_spec == 0) {
        apply(iplookup_table);
    }
    apply(switching_table);
}










