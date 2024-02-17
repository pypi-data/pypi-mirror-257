/******************************************************************************
 * kway_graph_refinement_commons.cpp 
 *
 * Source of KaHIP -- Karlsruhe High Quality Partitioning.
 *
 *****************************************************************************/

#include <omp.h>

#include "kway_graph_refinement_commons.h"

std::vector<kway_graph_refinement_commons*>* kway_graph_refinement_commons::m_instances = NULL;

kway_graph_refinement_commons::kway_graph_refinement_commons() {

}

kway_graph_refinement_commons::~kway_graph_refinement_commons() {
}


kway_graph_refinement_commons* kway_graph_refinement_commons::getInstance( PartitionConfig & config ) {

        bool created = false;
        #pragma omp critical 
        {
                if( m_instances == NULL ) {
                        m_instances = new std::vector< kway_graph_refinement_commons*>(omp_get_max_threads(), reinterpret_cast<kway_graph_refinement_commons*>(NULL));
                }
        } 

        int id = omp_get_thread_num();
        if((*m_instances)[id] == NULL) {
                (*m_instances)[id] = new kway_graph_refinement_commons();
                (*m_instances)[id]->init(config);
                created = true;
        }

        if(created == false) {
                if(config.k != (*m_instances)[id]->getUnderlyingK()) {
                        //should be a very rare case 
                        (*m_instances)[id]->init(config); 
                }
        }

        return  (*m_instances)[id];
}
